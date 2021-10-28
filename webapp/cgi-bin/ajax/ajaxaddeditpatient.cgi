#!/usr/bin/perl -w 

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "../globalfunctions.pl";

my $dbh = DBConnect();

SecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my %db = ();
if ( $in{patientid} ) {
    # We are editing
    my $sql = "select a.accountname, DATE_FORMAT(b.dob, '%d/%m/%Y') as dob, b.condition, b.height, b.weight 
            from ACCOUNT a 
            join PATIENT b on a.accountid=b.patientid 
            where patientid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    ( $db{accountname}, $db{dob}, $db{condition}, $db{height}, $db{weight} ) = $sth->fetchrow_array;
    $sth->finish();

    ( $db{firstname}, $db{lastname} ) = split( " ", $db{accountname} );

    $db{readonly} = "readonly";
    $db{readonly_bool} = 1;

} else {
    # We are not
}

my $filename = 'addeditpatient.tt';
my %args = (
    db => \%db
);

$main::g_template->process( $filename, \%args ) or die "Template process failed: " . $main::g_template->error();

$dbh->disconnect;

exit;
