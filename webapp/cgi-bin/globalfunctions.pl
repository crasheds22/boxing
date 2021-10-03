#!/usr/bin/perl -w

use strict;
use warnings;

use DBI;

sub DBConnect {

    my $host = "localhost";
    my $username = "slaveuser";
    my $password = "slavepass";
    my $port = 3306;
    my $tablespace = "boxing";

    my $dbi_str = "dbi:mysql:$tablespace;host=$host:$port";

    my $connector;
    eval {
        $connector = DBI->connect( $dbi_str, $username, $password, { AutoCommit => 0, RaiseError => 1 } );
        $connector->{LongReadLen} = 15005;
        $connector->{LongTruncOk} = 1;
    };

    if ( $@ ) {
        print STDERR "Error in connecting to DB";
        $connector = undef;
    }

    if ( $connector ) {
        return $connector;
    } else {
        exit;
    }

}

1;
