#!/usr/bin/perl -w

# TODO: removing is a form of saving

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SimpleSecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

$in{accounttypeid} = sprintf( "%d", $in{accounttypeid} );

my ( $sql, $sth );

print "Content-Type:text/json\n\n";
my $change ="";

if ( $in{clinicianid} ) {
    # We are editing

    $sql = "update ACCOUNT set accounttypeid=? where accountid=?";

    eval { 
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{accounttypeid} );
        $sth->finish();
    };
    if ( $@ ) {
        my %data = (
            success => 0,
            message => "Clinician update failed"
        );

        $dbh->rollback();
        $dbh->disconnect();

        print encode_json( \%data );
        exit;
    }

    $change = "updated";

} else {
    # We are creating

    my $accountname = $in{firstname} . " " . $in{lastname};

    $sql = "inset into ACCOUNT ( accountname, username, password, insertdate, timezone, accounttypeid )
            values ( ?, ?, 'Password1', UTC_TIMESTAMP(), '+8:00', ? )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $accountname, $in{username}, $in{accounttypeid} );
        $sth->finish();
    };
    if ( $@ ) {
        my %data = (
            success => 0,
            message => "Error creating new Account"
        );

        $dbh->rollback();
        $dbh->disconnect();

        print encode_json( \%data );
        exit;
    }

    my $clinicianid = $dbh->last_insert_id( undef, undef, undef, undef );

    $sql = "insert into CLINICIAN ( clinicianid )values ( ? )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $clinicianid );
        $sth->finish();
    };
    if ( $@ ) {
        my %data = (
            success => 0,
            message => "error creating Clinician"
        );

        $dbh->rollback();
        $dbh->disconnect();

        print encode_json( \%data );
        exit;
    }

    $sql = "insert into REPORTING ( headclinician, clinicianid ) values ( ?, ? )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $main::p{clinicianid}, $clinicianid );
        $sth->finish();
    };
    if ( $@ ) {
        my %data = (
            success => 0,
            message => "Error linking clinician"
        );

        $dbh->rollback();
        $dbh->disconnect();s

        print encode_json( \%data );
        exit;
    }

    $change = "created";
}

my %data = (
    success => 1,
    message => " Clinician $change"
);

$dbh->commit();
$dbh->disconnect();

print encode_json( \%data );

exit;
