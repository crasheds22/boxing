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
$in{sessionid} = $query->param('sessionid') ? sprintf( "%d", scalar $query->param('sessionid') ) : undef;

my ( $sql, $sth );
my %db = ();
my @patients = ();
my @activities = ();
my @clinicians = ();
my @exercises = ();

if ( $in{sessionid} ) {
    # Editing
    $sql = "select sessionid, sessionname, scheduledfor, patientid, clinicianid
            from SESSION
            where sessionid=? and !deleted";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{sessionid} );
    ( $db{sessionid}, $db{sessionname}, $db{scheduledfor}, $db{patientid}, $db{clinicianid} ) = $sth->fetchrow_array;
    $sth->finish;

    $sql = "select b.activityname, c.typename
            from EXERCISE a
            join ACTIVITY b on a.activityid=b.activityid
            join ACTIVITY_TYPE c on b.typeid=c.typeid
            where a.sessionid=?
            order by a.sessionorder";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $db{sessionid} );
    while ( my ( $exercisename, $exercisetype ) = $sth->fetchrow_array ) {
        push @exercises, qq^
            <tr>
                <td>$exercisename</td>
                <td>$exercisetype</td>
                <td><button type="button" class="btn btn-danger" onclick="RemoveExercise(this)"><span class="glyphicon glyphicon-minus"></span></button></td>
            </tr>
        ^;
    }

} else {
    # Creating
}

$sql = "select a.accountid, a.accountname 
        from ACCOUNT a
        join PATIENT b on a.accountid=b.patientid
        where b.insertby in ( -1, ? )";
$sth = $dbh->prepare( $sql );
$sth->execute( $main::p{accountid} );
while ( my ( $patientid, $patientname ) = $sth->fetchrow_array ) {
    push @patients, {
        id => $patientid,
        name => $patientname
    };
}
$sth->finish;

$sql = "select a.activityid, a.activityname, b.typename
        from ACTIVITY a
        join ACTIVITY_TYPE b on a.typeid=b.typeid
        where !a.deleted";
$sth = $dbh->prepare( $sql );
$sth->execute();
while ( my ( $activityid, $activityname, $typename ) = $sth->fetchrow_array ) {
    push @activities, qq^
        <tr data-attribute="$activityid">
            <td>$activityname</td>
            <td>$typename</td>
            <td><button type="button" class="btn btn-success" onclick="AddExercise(this)"><span class="glyphicon glyphicon-plus"></span></button></td>
        </tr>
    ^;
}
$sth->finish;

if ( $main::p{accounttypeid} != 3 ) {
    $sql = "select a.accountid, a.accountname
            from ACCOUNT a
            join CLINICIAN b on a.accountid=b.clinicianid
            join REPORTING c on b.clinicianid=c.clinicianid
            where c.headclinician=? and !deleted and !archived";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $main::p{clinicianid} );
    while ( my ( $clinicianid, $clinicianname ) = $sth->fetchrow_array ) {
        push @clinicians, {
            id => $clinicianid,
            name => $clinicianname
        };
    }
    $sth->finish;
}

my $filename = 'addeditsession.tt';
my %args = (
    p => \%main::p,
    db => \%db,
    patients => \@patients,
    clinicians => \@clinicians,
    activities => \@activities,
    exercises => \@exercises
);

$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error();

$dbh->disconnect;

exit;
