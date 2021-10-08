#!/usr/bin/perl -w

use DBI;

sub DBConnect {

    my $host = "db";
    my $username = "slaveuser";
    my $password = "slavepass";
    my $port = 3306;
    my $tablespace = "boxing";

    my $dbi_str = "dbi:mysql:database=$tablespace;host=$host;port=$port";

    my $connector = DBI->connect( $dbi_str, $username, $password, { AutoCommit => 0, RaiseError => 1 } );
    if ( !defined $connector ) {
        print STDERR $DBI::err . "\n" . $DBI::errstr;
        return undef;
    }
    $connector->{LongReadLen} = 15005;
    $connector->{LongTruncOk} = 1;

    if ( defined $connector ) {
        return $connector;
    } else {
        return undef;
    }

}

sub ACTIVEPage {

    my ( $pagename ) = @_;

    %ACTIVE = ();

    $ACTIVE{$pagename} = 'class="active"';

    return \%ACTIVE;

}

1;
