#!/usr/bin/perl -w

use DBI;
use Template;
use Digest::SHA qw( sha512_hex hmac_sha512_hex );
use Data::UUID;

use lib '/usr/lib/cgi-bin/lib';

use Boxing::Auth qw( GetAuthCookie SetAuthCookie );

$boxing_secret_key = 'Goj8EbUBND8oljJxpmX8mcVMbO2h4Djl';

%p = ();

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

sub SecurityCheck {

    my ( $dbh, $username ) = @_;

    print "Content-Type:text/html\n";

    if ( $username ) {
        Authenticate( $dbh, $username );
    } elsif ( my $sessionid = GetAuthCookie( "boxingsessionid" ) ) {
        CheckCookie( $dbh, $sessionid );

        if ( $in{logout} ) {
            Logout( $dbh, $sessionid, $p{accountid} );
        }
    } else {
        ShowLogin();
    }

    return;

}

sub Authenticate {

    my ( $dbh, $username ) = @_;

    my $sql = "select a.* 
            from ACCOUNT a
            where a.username like ?";
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
        &ShowError( "<p>This could mean your username is incorrect</p>", "Error logging in" );
        exit;
    }

    ( $p{sessionid} ) = &GenerateSessionID( $dbh, $p{accountid} );

    $sql = "insert into ACCOUNT_LOG ( accountid, insertdate, sessionid ) 
            values ( ?, UTC_TIMESTAMP(), ? )";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $p{accountid}, $p{sessionid} );
    $sth->finish;
    $dbh->commit;

    print SetAuthCookie( "boxingsessionid", $p{sessionid} );

    print "\n";

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
    $sth->execute( $p{sessionid} );
    my ( $ok, $accountid, $timeout ) = $sth->fetchrow_array;
    $sth->finish;

    if ( $ok && $timeout || !$ok ) {
        # Timeout
        &DestroySessionToken( $dbh, $sessionid );
        $dbh->disconnect;

        print SetAuthCookie( "boxingsessionid", "" );

        print "\n";
        ShowError( "<p>Session has timed out...</p>", "Session Timeout" );

        exit;

    } elsif ( $ok ) {
        &UpdateSessionToken( $dbh, $sessionid );
    }

    %p = ();
    $sql = "select a.* 
            from ACCOUNT a 
            where a.accountid = '?'";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $accountid );
    my $hashref = $sth->fetchrow_hashref;
    foreach ( keys %$hashref ) {
        $p{$_} = $hashref->{$_};
    }
    $sth->finish;

    return;

}

sub ShowLogin {

    print "\n";

    my $filename = 'login.tt';
    my %args = ();

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

    my $sql = "delete from ACCOUNT_SESSION where sessionid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $sessionid );
    $sth->finish();

    $dbh->commit();

    return;

}

1;
