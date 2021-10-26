#!/usr/bin/perl -w

use DBI;
use Template;
use Digest::SHA qw( sha512_hex hmac_sha512_hex );
use Data::UUID;

use lib '/usr/lib/cgi-bin/lib';

use Boxing::Auth qw( GetAuthCookie SetAuthCookie );

$boxing_secret_key = 'Goj8EbUBND8oljJxpmX8mcVMbO2h4Djl';

$g_template = Template->new(
    INCLUDE_PATH => '/usr/lib/html'
);

sub DBConnect {

    my $host = "db";
    my $username = "slaveuser";
    my $password = "slavepass";
    my $port = 3306;
    my $tablespace = "boxing";

    my $dbi_str = "dbi:mysql:database=$tablespace;host=$host;port=$port";

    my $connector = DBI->connect( $dbi_str, $username, $password, { AutoCommit => 0, RaiseError => 1 } );
    if ( !defined $connector ) {
        print STDERR $DBI::err . "\n" . $DBI::errstr;
        return undef;
    }
    $connector->{LongReadLen} = 15005;
    $connector->{LongTruncOk} = 1;

    if ( defined $connector ) {
        return $connector;
    } else {
        return undef;
    }

}

sub LogError {

    my ( $message ) = @_;

    print STDERR $message . "\n";

    return;

}

sub SecurityCheck {

    my ( $dbh, $in ) = @_;

    LogError( "Security Check Begin" );

    my %in = %$in if $in;

    print "Content-Type:text/html\n";

    if ( $in{username} ) {
        LogError( "Username detected: authenticating" );
        Authenticate( $dbh, $in{username} );
    } elsif ( my $sessionid = GetAuthCookie( "boxingsessionid" ) ) {
        LogError( "Checking sessionid: $sessionid") );
        CheckCookie( $dbh, $sessionid );

        if ( $in{logout} ) {
            LogError( "Log out request detected" );
            Logout( $dbh, $sessionid, $p{accountid} );
        }
    } else {
        LogError( "no data: showing login" );
        ShowLogin();
    }

    LogError( "End of security check" );

    print "\n";

    return;

}

sub Authenticate {

    my ( $dbh, $username ) = @_;

    %p = ();

    my $sql = "select accountid, accountname, insertdate, timezone, accounttypeid
            from ACCOUNT 
            where username = ? and !deleted and !archived";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $username );
    my $hashref = $sth->fetchrow_hashref;
    foreach ( keys %$hashref ) {
        $p{$_} = $hashref->{$_};
    }
    $sth->finish;

    if ( !$p{accountid} ) {
        print "\n";
        $dbh->disconnect;
        ShowError( "<p>This could mean your username is incorrect</p>", "Error logging in" );
        exit;
    }

    if ( $p{accounttypeid} == 4 ) {
        # A patient
        $sql = "select patientid, `condition`, dob, height, weight, armlength, insertby 
                from PATIENT 
                where patientid=?";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $p{accountid} );
        $hashref = $sth->fetchrow_hashref;
        foreach ( keys %$hashref ) {
            $p{$_} = $hashref->{$_};
        }
    } else {
        # A not patient
        $p{clinicianid} = $p{accountid};
        if ( grep { $p{accounttypeid} eq $_ } ( 1, 2 ) ) {
            $p{editclinician} = 1;
        }
    }

    my ( $sessionid ) = GenerateSessionID( $dbh, $p{accountid} );

    $sql = "insert into ACCOUNT_LOG ( accountid, insertdate, sessionid ) 
            values ( ?, UTC_TIMESTAMP(), ? )";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $p{accountid}, $sessionid );
    $sth->finish;
    $dbh->commit;

    print SetAuthCookie( "boxingsessionid", $sessionid );

}

sub GenerateSessionID {

    my ( $dbh, $accountid ) = @_;

    my $ug = Data::UUID->new;
    my $uuid = $ug->create_hex();
    my $payload = $uuid . $accountid;
    my $sessionid = hmac_sha512_hex( $payload, $boxing_secret_key );

    my $sql = "insert into ACCOUNT_SESSION ( sessionid, accountid, insertdate, last_seen ) 
            values ( ?, ?, UTC_TIMESTAMP(), UTC_TIMESTAMP() )";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $sessionid, $accountid );
    $sth->finish;

    $dbh->commit();

    return ( $sessionid );
}

sub CheckCookie {

    my ( $dbh, $sessionid ) = @_;

    # Timeout after 8 hours inactive;
    my $hoursTimeout = 8;

    my $sql = "select sessionid, accountid, last_seen < DATE_SUB(UTC_TIMESTAMP(), interval $hoursTimeout hour)
            from ACCOUNT_SESSION
            where sessionid = ?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $sessionid );
    my ( $ok, $accountid, $timeout ) = $sth->fetchrow_array;
    $sth->finish;

    if ( $ok && $timeout ) {
        # Timeout
        DestroySessionToken( $dbh, $sessionid );
        $dbh->disconnect;

        print SetAuthCookie( "boxingsessionid", "" );

        print "\n";
        ShowError( "<p>Session has timed out...</p>", "Session Timeout" );

        exit;

    } elsif ( $ok ) {
        UpdateSessionToken( $dbh, $sessionid );
    }

    if ( $accountid ) {
        %p = ();
        $sql = "select accountid, accountname, insertdate, timezone, accounttypeid
                from ACCOUNT 
                where accountid = ? and !deleted and !archived";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $accountid );
        my $hashref = $sth->fetchrow_hashref;
        foreach ( keys %$hashref ) {
            $p{$_} = $hashref->{$_};
        }
        $sth->finish;

        if ( $p{accounttypeid} == 4 ) {
            $sql = "select patientid, dob, `condition`, height, weight, armlength, insertby 
                    from PATIENT 
                    where patientid=?";
            $sth = $dbh->prepare( $sql );
            $sth->execute( $p{accountid} );
            $hashref = $sth->fetchrow_hashref;
            foreach ( keys %$hashref ) {
                $p{$_} = $hashref->{$_};
            }
            $sth->finish;
        } else {
            $p{clinicianid} = $p{accountid};
            if ( grep { $p{accounttypeid} eq $_ } ( 1, 2 ) ) {
                $p{editclinician} = 1;
            }
        }
    } else {
        $p{accountid} = 0;
    }

    return 1;

}

sub ShowLogin {

    my $filename = 'login.tt';
    my %args = ();

    print "\n";
    $g_template->process( $filename, \%args ) or die "Template process failed: " . $g_template->error();

    exit;

}

sub ActivePage {

    my ( $pagename ) = @_;

    my %ACTIVE = ();
    $ACTIVE{$pagename} = 'class="active"';

    return \%ACTIVE;

}

sub ShowError {

    my ( $error_msg, $error_title ) = @_;

    my $filename = 'Display/error.tt';
    my %args = (
        message => $error_msg,
        title => $error_title
    );

    print "\n";
    $g_template->process( $filename, \%args ) or die "Template process error: " . $g_template->error();

    exit;

}

sub DestroySessionToken {

    my ( $dbh, $sessionid ) = @_;

    my $sql = "delete 
            from ACCOUNT_SESSION 
            where sessionid = ?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $sessionid );
    $sth->finish();

    $dbh->commit();

    return;

}

sub Logout {

    my ( $dbh, $sessionid, $accountid ) = @_;

    DestroySessionToken( $dbh, $sessionid );
    print SetAuthCookie( "boxingsessionid", "" );

    my $sql = "update ACCOUNT_LOG
            set enddate=UTC_TIMESTAMP(), sessionid=null 
            where accountid=? and sessionid = ?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $accountid, $sessionid );
    $sth->finish();

    $dbh->commit();
    $dbh->disconnect;

    print "Location: http://localhost:8000/cgi-bin/login.cgi?logout=1\n\n";

    exit;

}

sub UpdateSessionToken {
    
    my ( $dbh, $sessionid ) = @_;

    my $sql = "update ACCOUNT_SESSION 
            set last_seen=UTC_TIMESTAMP() 
            where sessionid = ?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $sessionid );
    $sth->finish();

    $dbh->commit();

}

sub SimpleSecurityCheck {

    my ( $dbh ) = @_;

    my $sessionid = GetAuthCookie( "boxingsessionid" );
    
    if ( $sessionid eq "" ) {
        return 0;
    }

    return CheckCookie( $dbh, $sessionid );
}

sub MakeMYSQLDate {

    my ( $rawdate ) = @_;

    my ( $d, $m, $y ) = split( '/', $rawdate );

    my $formatted = "$y-$m-$d";

    return $formatted;

}

1;
