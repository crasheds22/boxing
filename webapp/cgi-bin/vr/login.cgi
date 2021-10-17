#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;

require "../globalfunctions.pl";

my $dbh = &DBConnect();

my $query = CGI->new();
my %in = ();
$in{username} = $query->param('username');
$in{password} = $query->param('password');

print "Content-Type: application/json\n\n";

if ( !$in{username} && !$in{password} ) {
    my %data = (
        success => 0,
        message => "You did not supply a username or password"
    );

    print encode_json( \%data );

    $dbh->disconnect();

    exit;
}

my ( $sql, $sth );

$sql = "select accountid, accountname, password from ACCOUNT where username like ?";
$sth = $dbh->prepare( $sql );
$sth->execute( $in{username} );
my ( $exists, $name, $password ) = $sth->fetchrow_array;
$sth->finish;

if ( $exists ) {
    my %data = (
        success => 1,
        message => "An account by the name of: $name, was found"
    );

    print encode_json( \%data );

    $dbh->disconnect();

    exit;

} else {
    my %data = (
        success => 0,
        message => "The username did not match any account"
    );

    print encode_json( \%data );

    $dbh->disconnect;

    exit;
}

exit;