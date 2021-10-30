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
$in{activityname} = $query->param('activity_name');
$in{activitytype} = sprintf( "%d", scalar $query->param('activity_type') );
$in{activityid} = $query->param('activityid') ? sprintf( "%d", scalar $query->param('activityid') ) : 0;
$in{delete} = $query->param('delete') ? 1 : 0;
my $data2 = $query->param('data');

print "Content-Type:application/json\n\n";

my ( $sql, $sth );
my %data = ();

if ( !$main::p{accountid} ) {
    # No accountid set, dont continue;
    %data = (
        success => \0,
        message => "Security Error"
    );
    print encode_json( \%data );
    $dbh->disconnect;
    exit;
}

if ( $in{delete} ) {
    $sql = "update ACTIVITY
            set deleted=1
            where activityid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{activityid} );
        $sth->finish();
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = \0;
        $data{message} = "Database delete failed";

        print encode_json( \%data );

        exit;
    }

} elsif ( $in{activityid} ) {
    $sql = "update ACTIVITY
            set activityname=?, instructions=?, typeid=?, modifieddate=UTC_TIMESTAMP()
            where activityid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute($in{activityname}, $data2, $in{activitytype}, $in{activityid});
        $sth->finish();
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = 0;
        $data{message} = "Database update failed";

        print encode_json( \%data );

        exit;
    }

} else {
    $sql = "insert into ACTIVITY (activityname, instructions, typeid, insertdate, modifieddate)
            values(?, ?, ?, UTC_TIMESTAMP(), UTC_TIMESTAMP())";
    eval { 
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{activityname}, $data2, $in{activitytype} );
        $sth->finish();
    };
    if ( $@ ) {
        $dbh->rollback();
        $dbh->disconnect();

        $data{success} = 0;
        $data{message} = "Database insert failed";

        print encode_json( \%data );

        exit;
    }
}

$dbh->commit();
$dbh->disconnect;

$data{success} = 1,;
$data{message} = "Activity Saved";

print encode_json( \%data );

exit;
