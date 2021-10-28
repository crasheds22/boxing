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
$in{clinicianid} = sprintf( "%d", scalar $query->param('clinicianid') );
$in{patientid} = sprintf( "%d", scalar $query->param('patientid') );
$in{exercises} = $query->param('exercises');
$in{sessionid} = $query->param('sessionid') ? sprintf( "%d", scalar $query->param('sessionid') ) : 0;
$in{delete} = $query->param('delete') ? 1 : 0;
$in{sessionname} = $query->param('sessionname');

$in{scheduledfor} = $query->param('scheduledfor');
$in{scheduledfor} = MakeMYSQLDate( $in{scheduledfor} );

my ( $sql, $sth );
my %data = ();

print "Content-Type:application/json\n\n";

if ( $in{delete} ) {
    $sql = "select sessionid from SESSION where sessionid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{sessionid} );
    my ( $ok ) = $sth->fetchrow_array();
    $sth->finish();

    if ( !$ok ) {
        $dbh->disconnect;
        
        %data = (
            success => \0,
            message => "Error: invalid sessionid\n"
        );

        print encode_json( \%data );

        exit;
    }

    $sql = "delete from EXERCISE 
            where sessionid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{sessionid} );
        $sth->finish;
    };
    if ( $@ ) {
        $dbh->rollback;
        $dbh->disconnect;

        %data = (
            success => \0,
            message => "Error deleting associated Exercises",
        );

        print encode_json( \%data );

        exit;
    }

    $sql = "update SESSION 
            set deleted=1
            where sessionid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{sessionid} );
        $sth->finish;
    };
    if ( $@ ) {
        $dbh->rollback;
        $dbh->disconnect;

        %data = (
            success => \0,
            message => "Error deleting Session",
        );

        print encode_json( \%data );

        exit;
    }

    %data = (
        success => \1,
        message => "Success: deleted Session"
    );

} elsif ( $in{sessionid} ) {
    $sql = "select sessionid from SESSION where sessionid=?";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{sessionid} );
    my ( $ok ) = $sth->fetchrow_array();
    $sth->finish();

    if ( !$ok ) {
        $dbh->disconnect;
        
        %data = (
            success => \0,
            message => "Error: invalid sessionid\n"
        );

        print encode_json( \%data );

        exit;
    }
    
    $sql = "update SESSION
            set sessionname=?, patientid=?, clinicianid=?, scheduledfor=?
            where sessionid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{sessionname}, $in{patientid}, $in{clinicianid}, $in{scheduledfor}, $in{sessionid} );
        $sth->finish;
    };
    if ( $@ ) {
        $dbh->rollback;
        $dbh->disconnect;

        %data = (
            success => \0,
            message => "Error updateing Session: $@\n"
        );

        print encode_json( \%data );

        exit;
    }

    $sql = "delete from EXERCISE
            where sessionid=?";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{sessionid} );
        $sth->finish;
    };
    if ( $@ ) {
        $dbh->rollback;
        $dbh->disconnect;

        %data = (
            success => \0,
            message => "Error deleting Exercises: $@\n"
        );

        print encode_json( \%data );

        exit;
    }

    my $count = 0;
    foreach ( @{ decode_json( $in{exercises} ) } ) {
        $sql = "insert into EXERCISE (sessionorder, sessionid, activityid)
                values (?, ?, ?)";
        eval {
            $sth = $dbh->prepare( $sql );
            $sth->execute( $count, $in{sessionid}, $_ );
            $sth->finish;
        };
        if ( $@ ) {
            $dbh->rollback;
            $dbh->disconnect;

            %data = (
                success => \0,
                message => "Error creating Exercise: $@\n"
            );

            print encode_json( \%data );

            exit;
        }

        $count++;
    }

    %data = (
        success => \1,
        message => "Session updated"
    );

} else {
    $sql = "insert into SESSION (sessionname, patientid, clinicianid, scheduledfor)
            values (?, ?, ?, ?)";
    eval {
        $sth = $dbh->prepare( $sql );
        $sth->execute( $in{sessionname}, $in{patientid}, $in{clinicianid}, $in{scheduledfor} );
        $sth->finish;
    };
    if ( $@ ) {
        $dbh->rollback;
        $dbh->disconnect;

        %data = (
            success => \0,
            message => "Error creating Session: $@\n"
        );

        print encode_json( \%data );

        exit;
    }

    my $sessionid = $sth->last_insert_id( undef, undef, undef, undef );

    my $count = 0;
    foreach ( @{ decode_json( $in{exercises} ) } ) {
        $sql = "insert into EXERCISE (sessionorder, sessionid, activityid)
                values (?, ?, ?)";
        eval {
            $sth = $dbh->prepare( $sql );
            $sth->execute( $count, $sessionid, $_ );
            $sth->finish;
        };
        if ( $@ ) {
            %data = (
                success => \0,
                message => "Error creating Exercise: $@\n"
            );

            $dbh->rollback;
            $dbh->disconnect();

            print encode_json( \%data );

            exit;
        }

        $count++;
    }

    %data = (
        success => \1,
        message => "Session successfully created"
    );
}

$dbh->commit();
$dbh->disconnect();

print encode_json( \%data );

exit;
