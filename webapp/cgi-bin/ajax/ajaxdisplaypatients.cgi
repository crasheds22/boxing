#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SimpleSecurityCheck( $dbh );

print "Content-Type; text/json\n\n";

my $query = CGI->new;
my %in = ();

my ( $sql, $sth );

my $insertby = "-1," . $main::p{clinicianid};

$sql = "select distinct a.accountname, b.patientid, b.dob, b.height, b.weight, b.condition
        from ACCOUNT a
        join PATIENT b on a.accountid=b.patientid
        where b.insertby in ( ? )";
$sth = $dbh->prepare( $sql );
$sth->execute( $insertby );
my @payload = ();
while ( my ( $accountname, $dob, $height, $weight, $condition ) = $sth->fetchrow_array ) {
    push @payload, {
        patientname => $accountname,
        dob => $dob,
        height => $height,
        weight => $weight,
        condition => $condition,
        edit => "<input type=\"button\" class=\"btn btn-primary btn-xs btn-outline\" onclick=\"EditPatient($patientid);\" />",
        delete => "<input type=\"button\" class=\"btn btn-danger btn-xs btn-outline\" onclick=\"RemovePatient($patientid);\" />"
    } 
}

print encode_json( \@payload );

exit;
