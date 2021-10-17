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

my $filename = 'dashboard.tt';
my %args = ();

$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error();

$dbh->disconnect();

exit;
