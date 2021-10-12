#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

exit;
#&SimpleSecurityCheck( $dbh );

if ( grep { $main::p{accounttypeid} ne $_ } ( 1, 2 ) ) {
    exit;
}

my $query = CGI->new;
my %in = ();
$in{headclinicianid} = sprintf( "%d", scalar $query->param('headclinicianid') );
$in{adminid} sprintf( "%d", scalar $query->param('adminid') );

my ( $sql, $sth );
my @payload = ();

if ( $in{headclinicianid} ) {
    # We want all clinicians reporting to this guy
    $sql = "select accountid, accountname 
            from ACCOUNT
            join REPORTING on accountid=clinicianid
            where headclinician=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{headclinician} );

} elsif ( $in{adminid} ) {
    # Lets just get all the head clinicians
    $sql = "select accountid, accountname
            from ACCOUNT
            where accounttypeid=2";
    $sth = $dbh->prepare( $sql );
    $sth->execute();
}

while ( my ( $clinicianid, $accountname ) = $sth->fetchrow_array ) {
    push @payload, {
        clinicianname => $accountname,
        edit => "<input type=\"button\" class=\"btn btn-xs btn-primary btn-outline\" onclick=\"EditClinician($clinicianid);\" />",
        delete => "<input type=\"button\" class=\"btn btn-xs btn-danger btn-outline\" onclick=\"RemoveClinician($clinicianid);\" />"
    };
}
$sth->finish;

print encode_json( \@payload );

exit;
