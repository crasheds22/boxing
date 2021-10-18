#!/usr/bin/perl -w 

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my %db = ();
if ( $in{patientid} ) {
    # We are editing
    my $sql = "select a.*, b.* 
            from ACCOUNT a 
            join PATIENT b on a.accountid=b.patientid 
            where patientid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{patientid} );
    my $hashref = $sth->fetchrow_hashref;
    while ( keys %{ $hashref } ) {
        $db{$_} = $hashref->{$_};
    }
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

print "Content-Type:text/html\n\n";
$main::g_template->process( $filename, \%args ) or die "Template process failed: " . $main::g_template->error();

$dbh->disconnect;

exit;
