#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "../globalfunctions.pl";

my $dbh = DBConnect();

SecurityCheck( $dbh );

if ( !$main::p{editclinician} ) {
    exit;
}

my $query = CGI->new();
my %in = ();
foreach ( $query->param ) {
    $in{$_} = $query->param($_);
}

my %db = ();
if ( $in{clinicianid} ) {
    # We are editing
    my $sql = "select a.*, b.*, c.*
            from ACCOUNT a
            join CLINICIAN b on a.accountid=b.clinicianid
            join ACCOUNT_TYPE c on a.accounttypeid=c.typeid
            where clinicianid=?";
    my $sth = $dbh->prepare( $sql );
    $sth->execute( $in{clinicianid} );
    my $hashref = $sth->fetchrow_hashref;
    $sth->finish;

    foreach ( keys %$hashref ) {
        $db{$_} = $hashref->{$_};
    }

    if ( $db{accounttypeid} == 3 ) {
        $db{clinician} = "selected";
    } elsif ( $db{accounttypeid} == 2 || $in{ishead} ) {
        $db{headclinician} = "selected";
    } elsif ( $db{accounttypeid} == 1 ) {
        $db{admin} = "selected";
    }

    ( $db{firstname}, $db{lastname} ) = split( " ", $db{accountname} );

    $db{readonly} = "readonly";
    $db{readonly_bool} = 1;

} else {
    # We are not
}

my $filename = "addeditclinician.tt";
my %args = (
    db => \%db,
    p => \%main::p
);

$main::g_template->process( $filename, \%args ) or die "Template process failed: " . $main::g_template->error();

exit;
