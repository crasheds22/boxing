#!/usr/bin/perl -w

use CGI;
use JSON;
use Template;

require "./globalfunctions.pl";

my $dbh = &DBConnect();

my $query = CGI->new();
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

&SecurityCheck( $dbh );

my $clinicianname;
if ( $in{clinicianid} && grep { $main::p{accounttypeid} eq $_ } ( 1, 2 ) ) {
    # We are viewing another clinician
    my $sql = "select accountname from ACCOUNT join CLINICIAN on accountid=clinicianid where clinicianid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{clinicianid} );
    ( $clinicianname ) = $sth->fetchrow_array;
    $sth->finish;

    $clinicianname .= "(Viewing)";
    
} else {
    $clinicianname = $in{accountname};
}

my $filename = 'clinician.tt';
my %args = (
    clinicianname => $clinicianname,
    activepage => &ActivePage( 'clinician' ),
    p => \%main::p
);

print "Content-Type:text/html\n\n";
$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error() . "\n";

$dbh->disconnect();

exit;
