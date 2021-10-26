#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();

my $query = CGI->new();
my %in = ();
$in{username} = $query->param('username');

print "Content-Type: application/json\n\n";

my %data = ();
if ( !$in{username} ) {
    %data = (
        success => 0,
        message => "You did not supply a username"
    );

    print encode_json( \%data );

    $dbh->disconnect();

    exit;
}

my ( $sql, $sth );

$sql = "select accountid
        from ACCOUNT 
        join PATIENT on accountid=patientid
        where username like ? and !deleted and !archived";
$sth = $dbh->prepare( $sql );
$sth->execute( $in{username} );
my ( $accountid ) = $sth->fetchrow_array;
$sth->finish;

if ( $accountid ) {

    my %db = ();

    $sql = "select b.patientid, a.accountname, a.timezone, b.dob, b.height, b.weight, b.armlength
            from ACCOUNT a
            join PATIENT b on b.patientid=a.accountid
            where a.accountid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $accountid );
    ( $db{Patient}{id},          $db{Patient}{accountname}, $db{Patient}{timezone}, 
      $db{Patient}{dob},         $db{Patient}{height}, 
      $db{Patient}{weight},      $db{Patient}{armlength} ) = $sth->fetchrow_array;
    $sth->finish;

    $sql = "select a.sessionid, c.accountname,
                DATE_FORMAT(DATE_ADD(a.scheduledfor, INTERVAL '$db{Patient}{timezone}' HOUR_MINUTE), '%d %m %Y') as scheduledfor
            from SESSION a 
            join CLINICIAN b on a.clinicianid=b.clinicianid
            join ACCOUNT c on b.clinicianid=c.accountid
            where a.patientid=? and a.completed is null and a.scheduledfor >= UTC_TIMESTAMP()
            limit 5";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $accountid );
    while ( my ( $sessionid, $accountname, $scheduledfor ) = $sth->fetchrow_array ) {
        my %session = (
            id => $sessionid,
            assignedby => $accountname,
            scheduledfor => $scheduledfor
        );
        
        $sql = "select a.exerciseid, a.sessionorder, b.activityname, b.instructions, c.typename
                from EXERCISE a
                join ACTIVITY b on a.activityid=b.activityid
                join ACTIVITY_TYPE c on b.typeid=c.typeid
                where a.sessionid=?";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $sessionid );
        while ( my ( $exerciseid, $sessionorder, $activityname, $instructions, $typename ) = $sth->fetchrow_array ) {
            push @{ $session{Exercise} }, {
                id => $exerciseid,
                activitytype => $typename,
                order => $sessionorder,
                activityname => $activityname,
                instructions => $instructions
            };
        }

        push @{ $db{Session} }, \%session;
    }

    %data = (
        data => \%db,
        success => \1,
        message => "Patient details retrieved"
    );

    print encode_json( \%data );

} else {
    %data = (
        success => 0,
        message => "The username did not match any active account"
    );

    print encode_json( \%data );

}

$dbh->disconnect;

exit;
