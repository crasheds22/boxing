#!/usr/bin/perl -w

# TODO: removing is a form of saving

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();

SimpleSecurityCheck( $dbh );

print "Content-Type:application/json\n\n";

my $query = CGI->new();
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my $editing = $in{patientid} ? 1 : 0;
$in{dob} = MakeMYSQLDate( $in{dob} );

my %data = ();
my ( $sql, $sth );

if ( !$main::p{accountid} ) {
    # No accountid set, dont continue;
    %data = (
        success => \0,
        message => "Security Error"
    );
    print encode_json( \%data );
    $dbh->disconnect;
    exit;
}

if ( $main::p{accounttypeid} == 4 ) {
    # This user is a patient and should not be here
    %data = (
        success => \0,
        message => "Security Error: invalid user access"
    );
    print encode_json( \%data );
    $dbh->disconnect;
    exit;
}

if ( $editing ) {
    $sql = "select patientid 
            from PATIENT 
            where patientid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    my ( $ok ) = $sth->fetchrow_array();
    $sth->finish();

    if ( !$ok ) {
        %data = (
            success => \0,
            message => "Not a real patient, cannot continue"
        );
        $dbh->disconnect;
        print encode_json( \%data );
        exit;
    }

    $sql = "select patientid 
            from PATIENT 
            where patientid=? and insertby in ( -1, ? )";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid}, $main::p{clinicianid} );
    ( $ok ) = $sth->fetchrow_array();
    $sth->finish();

    if ( !$ok ) {
        %data = (
            success => \0,
            message => "You do not have access to this patient"
        );
        $dbh->disconnect;
        print encode_json( \%data );
        exit;
    }
}

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
            set dob=?, `condition`=?, height=?, weight=?, insertby=?
            where patientid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{dob}, $in{condition}, $in{height}, $in{weight}, $in{patientid}, $db{whoaccess} );
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
    $sql = "insert into ACCOUNT ( accountname, insertdate, timezone, accounttypeid )
            values ( ?, UTC_TIMESTAMP(), '+8:00', 4 )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $accountname );
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

    $sql = "update ACCOUNT
            set username = LPAD( ?, 6, 0 )
            where accountid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $patientid, $patientid );
    };
    if ( $@ ) {
        $data{success} = \0;
        $data{message} = "Account creation error";

        print encode_json( \%data );

        $dbh->rollback();
        $dbh->disconnect();

        exit;
    }

    $sql = "insert into PATIENT ( patientid, dob, `condition`, height, weight, insertby )
            values ( ?, ?, ?, ?, ?, ? )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $patientid, $in{dob}, $in{condition}, $in{height}, $in{weight}, $db{whoaccess} );
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
