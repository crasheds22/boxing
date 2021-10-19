#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "./globalfunctions.pl";

my $dbh = &DBConnect();

&SecurityCheck( $dbh );

if ( !$main::p{accountid} ) {
    &ShowError( "Account error... see administrator", "Account Error" );
    exit;
}

if ( $main::p{accounttypeid} == 4 ) {
    &ShowError( "You do not have access to this area", "Security Error" );
    exit;
}

my $query = CGI->new();
my %in = ();
$in{clinicianid} = $query->param('clinicianid') ? sprintf( "%d", scalar $query->param('clinicianid') ) : 0;

my $clinicianname;
if ( $in{clinicianid} ) {
    # We are viewing another clinician
    my $sql = "select accountname 
            from ACCOUNT 
            join CLINICIAN on accountid=clinicianid 
            where clinicianid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{clinicianid} );
    ( $clinicianname ) = $sth->fetchrow_array;
    $sth->finish;

    $clinicianname .= "(Viewing)";
    
} else {
    $clinicianname = $main::p{accountname};
}

my $filename = 'clinician.tt';
my %args = (
    clinicianname => $clinicianname,
    activepage => &ActivePage( 'clinician' ),
    p => \%main::p
);

$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error() . "\n";

$dbh->disconnect();

exit;
