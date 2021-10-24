#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();

my $query = CGI->new;
my %in = ();
$in{armlength} = $query->param('armlength') ? sprintf( "%d", scalar $query->param('armlength') ) : 0;
$in{patientid} = $query->param('patientid') ? sprintf( "%d", scalar $query->param('patientid') ) : 0;

print "Content-Type:application/json\n\n";

my %data = ();
if ( !$in{armlength} ) {
    %data = (
        success => \0,
        message => "No arm length provided"
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
            message => "ID provided is not for any active patient, cannot continue"
        );

        $dbh->disconnect;

        print encode_json( \%data );
        
        exit;
    }

    $sql = "update PATIENT
            set armlength=?
            where patientid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{armlength}, $in{patientid} );
    $sth->finish();

    $dbh->commit;
    $dbh->disconnect();

    %data = (
        success => \1,
        message => "Patient arm length successfully updated"
    );

    print encode_json( \%data );

    exit;

} else {
    %data = (
        success => \0,
        message => "No patient id provided, cannot continue"
    );

    $dbh->disconnect();

    print encode_json( \%data );

    exit;
}

exit;
