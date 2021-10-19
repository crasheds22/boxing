#!/usr/bin/perl -w

# TODO: removing is a form of saving

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SimpleSecurityCheck( $dbh );

print "Content-Type:application/json\n\n";

my $query = CGI->new();
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my $editing = $in{patientid} ? 1 : 0;

my %data = ();
my ( $sql, $sth );

if ( $in{delete} ) {
    $sql = "update ACCOUNT 
            set deleted=1 
            where accountid=?";
    eval {    
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{patientid} );
        $sth->finish();
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = \0;
        $data{message} = "Error deleting patient";

        print encode_json( \%data );
        
        exit;
    }

    $data{success} = \1;
    $data{message} = "Patient deleted";

} elsif ( $in{archive} ) {
    $sql = "update ACCOUNT
            set archived=1
            where accountid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{patientid} );
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = \0;
        $data{message} = "Error archiving patient";

        print encode_json( \%data );
        
        exit;
    }

    $data{success} = \1;
    $data{message} = "Patient archived";

} elsif ( $editing ) {
    # Editing

    $sql = "update PATIENT 
            set dob=?, condition=?, height=?, weight=?
            where patientid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{dob}, $in{condition}, $in{height}, $in{width} );
        $sth->finish();
    };
    if ( $@ ) {
        $data{success} = \0;
        $data{message} = "Patient update error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    $data{success} = \1;
    $data{message} = "Patient updated";

} else {
    # Creating
    my $accountname = $in{firstname} . " " . $in{lastname};
    $sql = "insert into ACCOUNT ( accountname, username, password, insertdate, accounttypeid )
            values ( ?, ?, 'Password1', UTC_TIMESTAMP(), 4 )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $accountname, "$in{username}" );
    };
    if ( $@ ) {
        $data{success} = \0;
        $data{message} = "Account creation error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    my $patientid = $sth->last_insert_id( undef, undef, undef, undef );

    $in{dob} = &MakeMYSQLDate( $in{dob} );

    $sql = "insert into PATIENT ( patientid, dob, `condition`, height, weight, insertby )
            values ( ?, ?, ?, ?, ?, ? )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $patientid, $in{dob}, $in{condition}, $in{height}, $in{weight}, $main::p{clinicianid} );
        $sth->finish();
    };
    if ( $@ ) {
        $data{success} = 0;
        $data{message} = "Patient creation error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    $data{success} = \1;
    $data{message} = "Patient created";
}

$dbh->commit();
$dbh->disconnect();

print encode_json( \%data );

exit;
