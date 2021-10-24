#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "./globalfunctions.pl";

my $dbh = &DBConnect();

&SecurityCheck( $dbh );

my $filename = 'session.tt';
my %arg = (
    p => \%main::p,
    activepage => &ActivePage( 'session' )
);

$main::g_template->process( $filename, \%arg ) or die "Template process error: " . $main::g_template->error();

$dbh->disconnect;

exit;
