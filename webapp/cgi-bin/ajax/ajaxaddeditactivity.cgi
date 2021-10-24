#!/usr/bin/perl -w

use strict;
use warnings;

use CGI;
use JSON;
use Template;

require "../globalfunctions.pl";

my $dbh = DBConnect();

SecurityCheck( $dbh );

my $query = CGI->new();
my %in = ();
$in{activityid} = $query->param('activityid') ? sprintf( "%d", scalar $query->param('activityid') ) : undef;

my ( $sql, $sth );
my %db = ();

if ( $in{activityid} ) {
    # Editing
    $sql = "select activityid, activityname, instructions, typeid
            from ACTIVITY
            where activityid=? and !deleted";
    $sth = $dbh->prepare( $sql );
    $sth->execute( $in{activityid} );
    my $ok = 0;
    ( $db{activityid}, $db{activityname}, $db{instructions}, $db{typeid} ) = $sth->fetchrow_array;
    $sth->finish;

    my $struct = %{ decode_json( $db{instructions} ) };
    my $count = 1;
    foreach ( @$struct{Commands} ) {
        my ( $l, $r, $a ) = ( "", "", "" );
        if ( $_->{Hands} eq "Left" ) {
            $l = "selected";
        } elsif ( $_->{Hands} eq "Right" ) {
            $r = "selected";
        } elsif ( $_->{Hands} eq "Any" ) {
            $a = "selected";
        }

        $db{commands} .= qq^
            <tr>
                <td>$count</td>
                <td>$_->{TargetLocation}</td>
                <td width="100px"><input type="number" class="form-control" min="0" value="$_->{NumberOfHitsNeeded}" /></td>
                <td><select class="form-control"><option value=0 $a>A</option><option value=1 $l>L</option><option value=2 $r>R</option></select></td>
                <td width="100px"><input type="number" class="form-control" min="0" value="$_->{TimeBeforeDestruction}" /></td>
                <td align="right"><button type="button" class="btn btn-danger btn-xs" onclick="RemoveRow(this)"><span class="glyphicon glyphicon-minus"></span></button></td>
            </tr>
        ^;

        $count++;
    }

} else {
    # Creating
}

my @activity_types = ();
$sql = "select typeid, typename 
        from ACTIVITY_TYPE";
$sth = $dbh->prepare( $sql );
$sth->execute();
while ( my ( $id, $name ) = $sth->fetchrow_array ) {
    push @activity_types, {
        id => $id,
        name => $name
    };
}
$sth->finish;

my $filename = 'addeditactivity.tt';
my %args = (
    activity_types => \@activity_types,
    db => \%db,
    commands => $db{commands}
);

$main::g_template->process( $filename, \%args ) or die "Template process error: " . $main::g_template->error();

$dbh->disconnect();

exit;
