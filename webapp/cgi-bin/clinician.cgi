#!/usr/bin/perl -w 

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "./globalfunctions.pl";

my $query = CGI->new();
my %in = ();
foreach ( $query->param() ) {
    $in{$_} = $query->param($_);
}

my $dbh = &DBConnect();

my $filename = "clinician.tt";

my $template = Template->new(
    INCLUDE_PATH => '/usr/lib/html'
);

my $clinicianname;
if ( ( $main::p{accounttypeid} == 2 or $main::p{accounttypeid} == 1 ) and defined $in{clinicianid} ) {
    #User is viewing a clinician
    my $sql = "select accountname from ACCOUNT where accountid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{clinicianid} );
    ( $clinicianname ) = $sth->fetchrow_array();
    $sth->finish();

    $clinicianname .= " (Viewing)";
}

&ACTIVEPage( 'clinician' );

my %args = (
    clinicianname => $clinicianname,
    ACTIVE => \%main::ACTIVE,
    p => \%main::p
);

print "Content-Type: text/html\n\n";
$template->process( $filename, \%args ) or die "Template process failed (clinician): ", $template->error();

$dbh->disconnect();

exit;
