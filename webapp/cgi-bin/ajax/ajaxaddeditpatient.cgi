#!/usr/bin/perl -w 

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "../globalfunctions.pl";

my $dbh = DBConnect();

SecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my ( $sql, $sth );
my %db = ();

if ( $in{patientid} ) {
    # We are editing
    $sql = "select b.patientid, a.username, a.accountname, DATE_FORMAT(b.dob, '%d/%m/%Y') as dob, b.condition, b.height, b.weight, b.insertby 
            from ACCOUNT a 
            join PATIENT b on a.accountid=b.patientid 
            where patientid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    ( $db{patientid}, $db{username}, $db{accountname}, $db{dob}, $db{condition}, $db{height}, $db{weight}, $db{insertby} ) = $sth->fetchrow_array;
    $sth->finish();

    ( $db{firstname}, $db{lastname} ) = split( " ", $db{accountname} );

    $db{readonly} = "readonly";
    $db{readonly_bool} = 1;

} else {
    # We are not
}

my @clinicians = ();
$sql = "select accountid, accountname 
        from ACCOUNT 
        join CLINICIAN on accountid=clinicianid";
$sth = $dbh->prepare( $sql );
$sth->execute();
while ( my ( $id, $name ) = $sth->fetchrow_array ) {
    push @clinicians, {
        id => $id,
        name => $name
    };
}
$sth->finish;

my $filename = 'addeditpatient.tt';
my %args = (
    db => \%db,
    clinicians => \@clinicians
);

$main::g_template->process( $filename, \%args ) or die "Template process failed: " . $main::g_template->error();

$dbh->disconnect;

exit;
