#!/usr/bin/perl -w

use strict;
use warnings;

use Template;

require "./globalfunctions.pl";

my $filename = "login.tt";

my $template = Template->new(
    INCLUDE_PATH => '/usr/lib/html/'
);

my %args = ();

print "Content-Type: text/html\n\n";
$template->process( $filename, \%args ) or die "Template process failed (login): ", $template->error();

exit; 
