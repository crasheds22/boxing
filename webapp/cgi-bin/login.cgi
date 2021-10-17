#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "./globalfunctions.pl";

my $dbh = &DBConnect();

my %in = ();
my $query = CGI->new();
$in{username} = $query->param('username');

&SecurityCheck( $dbh, $in{username} );

if ( $main::p{accounttypeid} == 4 ) {
    # Patient
    print STDERR "A patient has logged in\n";
    $dbh->disconnect();
} else {
    # Not a patient
    print STDERR "A not patient has logged in\n";
    $dbh->disconnect();
}

exit;
