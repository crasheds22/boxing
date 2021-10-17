#!/usr/bin/perl -w

package Boxing::Auth;

use strict;
use warnings;

use Exporter qw( import );
use CGI::Cookie;

our @EXPORT_OK = qw( GetAuthCookie SetAuthCookie );

sub SetAuthCookie {

    my ( $cookie_name, $sessionid ) = @_;

    die "No cookie name defined" unless $cookie_name;
    die "No session id provided" unless defined $sessionid;

    my $cookie_args = {
        -name => $cookie_name,
        -value => $sessionid,
        -path => '/',
        -httponly => \1,
        -samesite => 'Lax',
        -expires => '+12h',
        -secure => \1
    };

    my $cookie = CGI::Cookie->new( $cookie_args );

    my $cookie_header = 'Set-Cookie: ' . $cookie->as_string;

    my $cache_header = 'Cache-Control: no-store';

    return "$cookie_header\n$cache_header\n";

}

sub GetAuthCookie {

    my ( $cookie_name ) = @_;

    my %cookies = CGI::Cookie->fetch;

    return defined $cookies{$cookie_name} ? $cookies{$cookie_name}->value : undef;

}
