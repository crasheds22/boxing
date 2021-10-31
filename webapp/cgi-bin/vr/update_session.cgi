#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();

my $query = CGI->new;
my %in = ();
my $rawput = $query->param('PUTDATA');

my $decoded_json = decode_json( $rawput );

$in{patientid} = $decoded_json->{patientid};
$in{sessionid} = $decoded_json->{sessionid};
$in{exercisedata} = $decoded_json->{exercisedata};

my %data = ();

print "Content-Type:application/json\n\n";

if ( !$in{sessionid} ) {
    %data = (
        success => \0,
        message => "No session id provided, cannot continue\n"
    );

    $dbh->disconnect;

    print encode_json( \%data );

    exit;
}

if ( !$in{patientid} ) {
    %data = (
        success => \0,
        message => "No patient id provided, cannot continue\n"
    );

    $dbh->disconnect;
    
    print encode_json( \%data );

    exit;
}

my ( $sql, $sth );

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

$sql = "update EXERCISE
        set exercisedata=?
        where exerciseid=?";
$sth = $dbh->prepare( $sql );
$sth->execute( $in{exercisedata}->{data}, $in{exercisedata}->{id} );
$sth->finish;

$sql = "select count(exerciseid)
        from EXERCISE
        where exercisedata is not null and sessionid=?";
$sth = $dbh->prepare( $sql );
$sth->execute( $in{sessionid} );
my ( $incomplete ) = $sth->fetchrow_array();
$sth->finish;

if ( !$incomplete ) {
    $sql = "update SESSION
            set completed=UTC_TIMESTAMP()
            where sessionid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{sessionid} );
    $sth->finish;
}

$dbh->commit;
$dbh->disconnect;

%data = (
    success => \1,
    message => "Session for patient successfully updated\n"
);

print encode_json( \%data );


exit;
