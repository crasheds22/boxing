#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SimpleSecurityCheck( $dbh );

print "Content-Type:application/json\n\n";

my $query = CGI->new;
my %in = ();
$in{headclinicianid} = $query->param('headclinicianid') ? sprintf( "%d", scalar $query->param('headclinicianid') ) : 0;
$in{adminid} = $query->param('adminid') ? sprintf( "%d", scalar $query->param('adminid') ) : 0;

my ( $sql, $sth );
my %payload = ( data => [] );

if ( $in{headclinicianid} ) {
    # We want all clinicians reporting to this guy
    $sql = "select accountid, accountname 
            from ACCOUNT
            join REPORTING on accountid=clinicianid
            where headclinician=? and !deleted and !archived";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{headclinicianid} );

} elsif ( $in{adminid} ) {
    # Lets just get all the head clinicians
    $sql = "select accountid, accountname
            from ACCOUNT
            where accounttypeid = 2 and !deleted and !archived";
    $sth = $dbh->prepare( $sql );
    $sth->execute();


} else {
    $dbh->disconnect();
    print STDERR "No head clinician or admin id\n";
    print encode_json( \%payload );
    exit;
}

while ( my ( $clinicianid, $accountname ) = $sth->fetchrow_array ) {
    push @{ $payload{data} }, {
        clinicianname => $accountname,
        edit => "<input type=\"button\" class=\"btn btn-xs btn-primary btn-outline\" onclick=\"EditClinician($clinicianid);\" value=\"Edit\" />",
        delete => "<input type=\"button\" class=\"btn btn-xs btn-danger btn-outline\" onclick=\"RemoveClinician($clinicianid);\" value=\"Delete\" />"
    };
}
$sth->finish;

$dbh->disconnect();

print encode_json( \%payload );

exit;
