#!/usr/bin/perl -w

# TODO: removing is a form of saving

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

exit;
#&SimpleSecurityCheck();

my $query = CGI->new();
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my $editing = defined $in{patientid} ? 1 : 0;

my %data = ();
my ( $sql, $sth );

if ( $editing ) {
    # Editing

    eval {
        $sql = "update PATIENT 
                set dob=?, condition=?, height=?, weight=?
                where patientid=?";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{dob}, $in{condition}, $in{height}, $in{width} );
        $sth->finish();
    };
    if ( $@ ) {
        $data{success} = 0;
        $data{message} = "Patient update error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    $data{success} = 1;
    $data{message} = "Patient updated";

} else {
    # Creating

    eval {
        my $accountname = $in{firstname} . " " . $in{lastname};
        $sql = "insert into ACCOUNT ( accountname, username, password, insertdate, accounttypeid )
                values ( ?, ?, 'Password1', UTC_TIMESTAMP(), 4 )";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $accountname, $in{username} );
    };
    if ( $@ ) {
        $data{success} = 0;
        $data{message} = "Account creation error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    my $patientid = $sth->last_insert_id( undef, undef, undef, undef );

    eval {
        $sql = "insert into PATIENT ( patientid, dob, condition, height, weight, insertby )
                values ( ?, ?, ?, ?, ?, ? )";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $patientid, $in{dob}, $in{condition}, $in{height}, $in{width}, $main::p{clinicianid} );
        $sth->finish();
    }:
    if ( $@ ) {
        $data{success} = 0;
        $data{message} = "Patient creation error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    $data{success} = 1;
    $data{message} = "Patient created";
}

$dbh->disconnect();
$dbh->commit();

print encode_json( \%data );

exit;
