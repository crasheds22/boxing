#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = DBConnect();
SimpleSecurityCheck( $dbh );

my $query = CGI->new;
my %in = ();
$in{patientid} = $query->param('patientid') ? sprintf( "%d", scalar $query->param('patientid') ) : 0;
$in{clinicianid} = $query->param('clinicianid') ? sprintf( "%d", scalar $query->param('clinicianid') ) : 0;
$in{iscompleted} = $query->param('iscompleted') ? 1 : 0;

print "Content-Type:application/json\n\n";

my ( $sql, $sth );
my %payload = ( data => [] );

if ( $in{patientid} ) {
    # Patient specific
    if ( $in{iscompleted} ) {
        $sql = "select a.sessionid, a.sessionname, 
                    DATE_FORMAT(DATE_ADD(a.scheduledfor, INTERVAL '%main::p{timezone}' HOUR_MINUTE), '%d %b %Y') as scheduledfor, c.accountname,
                    DATE_FORMAT(DATE_ADD(a.completed, INTERVAL '%main::p{timezone}' HOUR_MINUTE), '%d %b %Y') as completed
                from SESSION a
                join CLINICIAN b on a.clinicianid=b.clinicianid
                join ACCOUNT c on b.clinicianid=c.accountid
                where a.patientid=? and a.completed is not null and !a.deleted";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{patientid} );
        while ( my ( $sessionid, $sessionname, $scheduledfor, $assignedby, $completedon ) = $sth->fetchrow_array ) {
            push @{ $payload{data} }, {
                sessionname => $sessionname,
                scheduledfor => $scheduledfor,
                completedon => $completedon,
                assignedby => $assignedby,
                buttons => qq^
                    <input type="button" class="btn btn-default" onclick="ViewSession($sessionid)" value="View" />
                ^
            };
        }
        $sth->finish;

    } else {
        $sql = "select a.sessionid, a.sessionname, DATE_FORMAT( DATE_ADD( a.scheduledfor, INTERVAL '%main::p{timezone}' HOUR_MINUTE ), '%d %b %Y' ) as scheduledfor, c.accountname,
                    a.scheduledfor < UTC_TIMESTAMP() as overdue
                from SESSION a
                join CLINICIAN b on a.clinicianid=b.clinicianid
                join ACCOUNT c on b.clinicianid=c.accountid
                where a.patientid=? and a.completed is null and !a.deleted";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{patientid} );
        while ( my ( $sessionid, $sessionname, $scheduledfor, $assignedby, $overdue ) = $sth->fetchrow_array ) {
            if ( $overdue ) {
                $scheduledfor = qq^
                    <span class="badge badge-warning">$scheduledfor</span>
                ^;
            }
            push @{ $payload{data} }, {
                sessionname => $sessionname,
                scheduledfor => $scheduledfor,
                assignedby => $assignedby,
                buttons => qq^
                    <input type="button" class="btn btn-default" onclick="ViewSession($sessionid)" value="View" />
                ^
            };
        }
        $sth->finish;

    }

} elsif ( $in{clinicianid} ) {
    # Clinician specific
    if ( $in{iscompleted} ) {
        $sql = "select a.sessionid, a.sessionname, 
                    DATE_FORMAT(DATE_ADD(a.scheduledfor, INTERVAL '%main::p{timezone}' HOUR_MINUTE), '%d %b %Y') as scheduledfor, c.accountname,
                    DATE_FORMAT(DATE_ADD(a.completed, INTERVAL '%main::p{timezone}' HOUR_MINUTE), '%d %b %Y') as completed
                from SESSION a
                join PATIENT b on a.patientid=b.patientid
                join ACCOUNT c on b.patientid=c.accountid
                where a.clinicianid=? and a.completed is not null and !a.deleted";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{clinicianid} );
        while ( my ( $sessionid, $sessionname, $scheduledfor, $assignedto, $completedon ) = $sth->fetchrow_array ) {
            push @{ $payload{data} }, {
                sessionname => $sessionname,
                scheduledfor => $scheduledfor,
                completedon => $completedon,
                assignedto => $assignedto,
                buttons => qq^
                    <input type="button" class="btn btn-success btn-xs btn-outline" onclick="ViewSession($sessionid)" value="View" />
                ^
            };
        }
        $sth->finish;

    } else {
        $sql = "select a.sessionid, a.sessionname, DATE_FORMAT(DATE_ADD(a.scheduledfor, INTERVAL '%main::p{timezone}' HOUR_MINUTE), '%d %b %Y') as scheduledfor, c.accountname,
                    a.scheduledfor < UTC_TIMESTAMP() as overdue
                from SESSION a
                join PATIENT b on a.patientid=b.patientid
                join ACCOUNT c on b.patientid=c.accountid
                where a.clinicianid=? and a.completed is null and !a.deleted";
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{clinicianid} );
        while ( my ( $sessionid, $sessionname, $scheduledfor, $assignedto, $overdue ) = $sth->fetchrow_array ) {
            if ( $overdue ) {
                $scheduledfor = qq^
                    <span class="badge badge-warning">$scheduledfor</span>
                ^;
            }
            push @{ $payload{data} }, {
                sessionname => $sessionname,
                scheduledfor => $scheduledfor,
                assignedto => $assignedto,
                buttons => qq^
                    <input type="button" class="btn btn-primary btn-xs btn-outline" onclick="EditSession($sessionid);" value="Edit" />&nbsp;
                    <input type="button" class="btn btn-danger btn-xs btn-outline" onclick="DeleteSession($sessionid);" value="Delete" />
                ^
            };
        }
        $sth->finish;

    }

} else {
    $dbh->disconnect;
    print encode_json( \%payload );
    exit;
}

$dbh->disconnect();

print encode_json( \%payload );

exit;
