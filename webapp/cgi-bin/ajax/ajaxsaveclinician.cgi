#!/usr/bin/perl -w

# TODO: removing is a form of saving

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();

SimpleSecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

$in{accounttypeid} = sprintf( "%d", $in{accounttypeid} );

my ( $sql, $sth );
my %data = ();

print "Content-Type:application/json\n\n";

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

if ( $in{delete} ) {
    $sql = "update ACCOUNT 
            set deleted=1 
            where accountid=?";
    
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{clinicianid} );
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = \0;
        $data{message} = "Error deleting Clinician";

        print encode_json( \%data );

        exit;
    }

    $data{success} = \1;
    $data{message} = "Clinician deleted"


} elsif ( $in{archive} ) {
    $sql = "update ACCOUNT 
            set archived=1 
            where accountid=?";
    
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{clinicianid} );
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = \0;
        $data{message} = "Error archiving Clinician";

        print encode_json( \%data );

        exit;
    }

    $data{success} = \1;
    $data{message} = "Clinician archived";


} elsif ( $in{clinicianid} ) {
    # We are editing

    $sql = "update ACCOUNT 
            set accounttypeid=? 
            where accountid=?";

    eval { 
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{accounttypeid}, $in{clinicianid} );
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

    $data{success} = \1;
    $data{message} = "Clinician Updated";

} else {
    # We are creating

    my $accountname = $in{firstname} . " " . $in{lastname};

    $sql = "insert into ACCOUNT ( accountname, insertdate, timezone, accounttypeid )
            values ( ?, UTC_TIMESTAMP(), '+8:00', ? )";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $accountname, $in{accounttypeid} );
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

    $sql = "update ACCOUNT 
            set username = LPAD( ?, 6, 0 ) 
            where accountid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $clinicianid, $clinicianid );
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

    $sql = "insert into CLINICIAN ( clinicianid )
            values ( ? )";
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

    $sql = "insert into REPORTING ( headclinician, clinicianid ) 
            values ( ?, ? )";
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
        $dbh->disconnect();

        print encode_json( \%data );
        exit;
    }

    $data{success} = \1;
    $data{message} = "Clinician created";
}

$dbh->commit();
$dbh->disconnect();

print encode_json( \%data );

exit;
