#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "./globalfunctions.pl";

my $dbh = DBConnect();

SecurityCheck( $dbh );

if ( !$main::p{accountid} ) {
    ShowError( "Account Error... see administrator", "Account Error" );
    exit;
}

my $query = CGI->new();
my %in = ();
$in{patientid} = $query->param('patientid') ? sprintf( "%d", scalar $query->param('patientid') ) : 0;

my $patientname;
if ( $in{patientid} ) {
    # We are a clinician viewing a patient
    my $sql = "select accountname 
            from ACCOUNT 
            join PATIENT on accountid=patientid
            where patientid=?";
    my $sth =$dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    ( $patientname ) = $sth->fetchrow_array;
    $sth->finish;

    $patientname .= " (Viewing)";

} else {
    $patientname = $main::p{accountname};
}

my $filename = "patient.tt";
my %args = (
    patientname => $patientname,
    activepage => ActivePage( 'patient' ),
    p => \%main::p,
    i => \%in
);

$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error();

$dbh->disconnect();

exit;
