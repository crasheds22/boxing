#!/usr/bin/perl -w

use strict;
use warnings;

use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SimpleSecurityCheck( $dbh );

my ( $sql, $sth );

my $insertby = "-1," . $main::p{clinicianid};

$sql = "select distinct a.accountname, b.patientid, b.dob, b.height, b.weight, b.condition
        from ACCOUNT a
        join PATIENT b on a.accountid=b.patientid
        where b.insertby in ( ? )";
$sth = $dbh->prepare( $sql );
$sth->execute( $insertby );
my %payload = ( data => [] );
while ( my ( $accountname, $patientid, $dob, $height, $weight, $condition ) = $sth->fetchrow_array ) {
    my $row = {
        patientname => $accountname,
        dob => $dob,
        height => $height,
        weight => $weight,
        condition => $condition,
        edit => "<input type=\"button\" class=\"btn btn-primary btn-xs btn-outline\" onclick=\"EditPatient($patientid);\" />",
        delete => "<input type=\"button\" class=\"btn btn-danger btn-xs btn-outline\" onclick=\"RemovePatient($patientid);\" />"
    };

    push @{ $payload{data} }, $row;
}

$dbh->disconnect;

print "Content-Type: application/json\n\n";
print encode_json( \%payload );

exit;
