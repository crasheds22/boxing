#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();

my $query = CGI->new;
my %in = ();
$in{patientid} = $query->param('patientid') ? sprintf( "%d", scalar $query->param('patientid') ) : 0;
$in{sessionid} = $query->param('sessionid') ? sprintf( "%d", scalar $query->param('sessionid') ) : 0;
$in{exercisedata} = $query->param('exercisedata');

my %data = ();

if ( !$in{sessionid} ) {
    %data = (
        success => \0,
        message => "No session id provided, cannot continue\n"
    );

    $dbh->disconnect;

    print encode_json( \%data );

    exit;
}

my ( $sql, $sth );

if ( $in{patientid} ) {
    $sql = "select patientid 
            from PATIENT 
            join ACCOUNT on patientid=accountid 
            where patientid=? and !deleted and !archived";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    my ( $ok ) = $sth->fetchrow_array;
    $sth->finish;

    if ( !$ok ) {
        %data = (
            success => \0,
            message => "ID provided is not for any active patient, cannot continue\n"
        );

        $dbh->disconnect;

        print encode_json( \%data );

        exit;
    }

    $sql = "select sessionid 
            from SESSION 
            where sessionid=? and patientid=? and completed is null";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{sessionid}, $in{patientid} );
    ( $ok ) = $sth->fetchrow_array;
    $sth->finish;

    if ( !$ok ) {
        %data = (
            success => \0,
            message => "ID provided is not for any incomplete session for this patient, cannot continue"
        );

        $dbh->disconnect;

        print encode_json( \%data );

        exit;
    }

    foreach ( @{ decode_json( $in{exercisedata} ) } ) {
        $sql = "update EXERCISE
                set exercisedata=?
                where exerciseid=?";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $_->{data}, $_->{id} );
        $sth->finish;
    }

    $sql = "update SESSION
            set completed=UTC_TIMESTAMP()
            where sessionid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{sessionid} );
    $sth->finish;

    $dbh->commit;
    $dbh->disconnect;

    %data = (
        success => \1,
        message => "Session for patient successfully updated\n"
    );

    print encode_json( \%data );

    exit;

} else {
    %data = (
        success => \0,
        message => "No patient id provided, cannot continue\n"
    );

    $dbh->disconnect;
    
    print encode_json( \%data );

    exit;
}


exit;
