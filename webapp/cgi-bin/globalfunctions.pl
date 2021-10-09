#!/usr/bin/perl -w

use DBI;
use Template;

%p = ();
$sessionid = undef;

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

    my ( $dbh, $in ) = @_;

    my %in = %$in if defined $in;

    print "Content-Type:text/html\n\n";

    if ( $in{username} && $in{password} ) {
        Authenticate( $dbh, $in{username}, $in{password} );
    #} elsif ( $sessionid ) {
    #    CheckCookie();
    } else {
        ShowLogin();
    }

}

sub Authenticate {

    my ( $dbh, $username, $password ) = @_;

    my $sql = "select accountid, accountname, username, password, insertdate, timezone, accounttypeid
            from ACCOUNT
            where username like ? and !archived and !deleted";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $username );
    my $hashref = $sth->fetchrow_hashref();
    foreach ( keys %$hashref ) {
        $p{$_} = $hashref->{$_};
    }
    $sth->finish;

    # TODO: password magic

    if ( $p{accounttypeid} == 4 ) {
        # We have a patient
        $sql = "select a.patientid, a.dob, a.condition, a.height, a.weight, a.armlength, a.insertby
                from PATIENT a
                where a.patientid=?";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $p{accountid} );
        $hashref = $sth->fetchrow_hashref();
        foreach ( keys %$hashref ) {
            $p{$_} = $hashref->{$_};
        }
        $sth->finish;
    } else {
        # We have an Admin, Head Clinician or Clinician
        $p{clinicianid} = $p{accountid};
    }

    # Generate sessionid

}

sub CheckCookie {

}

sub ShowLogin {

    my $filename = 'login.tt';

    my %args = (

    );

    $g_template->process( $filename, \%args ) or die "Template process error: " . $g_template->error() . "\n";

    return;

}

1;
