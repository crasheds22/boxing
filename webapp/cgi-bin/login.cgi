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
$in{logout} = scalar $query->param('logout') ? 1 : 0;

&SecurityCheck( $dbh, \%in );

my $filename = 'dashboard.tt';
my %args = (
    p => \%main::p
);

$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error();

$dbh->disconnect();

exit;
