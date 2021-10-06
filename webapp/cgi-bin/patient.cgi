#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "./globalfunctions.pl";

my $query = CGI->new();
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my $dbh = &DBConnect();

my $filename = "patient.tt";

my $template = Template->new(
    INCLUDE_PATH => '/usr/lib/html'
);

my $patientname;
if ( $main::p{accounttypeid} == 4 ) {
    # User is a patient
    $patientname = $main::p{accountname};
} else {
    # User is viewing a patient
    my $sql = "select accountname from ACCOUNT where accountid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    ( $patientname ) = $sth->fetchrow_array();
    $sth->finish;

    $patientname .= " (Viewing)";
}

&ACTIVEPage( 'patient' );

my %args = (
    patientname => $patientname,
    ACTIVE => \%main::ACTIVE,
    p => \%main::p
);

print "Content-Type:text/html\n\n";
$template->process( $filename, \%args ) or die "Template process failed (patient): ", $template->error();

$dbh->disconnect();

exit;
