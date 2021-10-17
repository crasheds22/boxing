#!/usr/bin/perl -w

use DBI;
use Template;

%p = ();
$sessionid = undef;

$g_template = Template->new(
    INCLUDE_PATH => '/usr/lib/html'
);

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

sub SecurityCheck {

    my ( $dbh, $in ) = @_;

    my %in = %$in if defined $in;

    ShowLogin();

}

sub Authenticate {



}

sub CheckCookie {

}

sub ShowLogin {

    my $filename = 'login.tt';

    my %args = (

    );

    $g_template->process( $filename, \%args ) or die "Template process error: " . $g_template->error() . "\n";

    return;

}

sub ActivePage {

    my ( $pagename ) = @_;

    my %ACTIVE = ();
    $ACTIVE{$pagename} = 'class="active"';

    return \%ACTIVE;
}

1;
