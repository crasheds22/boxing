#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

&SimpleSecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();

print "Content-Type:application/json\n\n";

my ( $sql, $sth );
my %payload = ( data => [] );

$sql = "select a.activityid, a.activityname, b.typename, 
            DATE_FORMAT(DATE_ADD(a.modifieddate, INTERVAL '$main::p{timezone}' HOUR_MINUTE), '%d %m %Y') as modifieddate,
            DATE_FORMAT(DATE_ADD(a.insertdate, INTERVAL '$main::p{timezone}' HOUR_MINUTE), '%d %m %Y') as insertdate
        from ACTIVITY a
        join ACTIVITY_TYPE b on a.typeid=b.typeid";
$sth = $dbh->prepare( $sql );
$sth->execute();
while ( my ( $activityid, $activityname, $activitytype, $modifieddate, $insertdate ) = $sth->fetchrow_array ) {
    push @{ $payload{data} }, {
        activityname => $activityname,
        activitytype => $activitytype,
        insertdate => $insertdate,
        modifieddate =>  $modifieddate,
        buttons => qq^
            <input type="button" class="btn btn-primary btn-xs btn-outline" onclick="EditActivity($activityid);" value="Edit" />&nbsp;
            <input type="button" class="btn btn-danger btn-xs btn-outline" onclick="DeleteActivity($activityid);" value="Delete" />
        ^
    };
}
$sth->finish;

print encode_json( \%payload );

exit;
