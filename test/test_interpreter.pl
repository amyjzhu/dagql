use warnings;
use strict;

our $__DAGQL_TESTS_FAILED__ = 0;

sub assert_output {
    my ( $string, $exp_out ) = @_;
    my ( undef, $filename, $line ) = caller;

    my $RED = "\x1B[31m";
    my $END = "\x1B[0m";

    my $output = qx+python3 -m dagql test/inputs/$string+;

    if ($output ne $exp_out) {
        print "$RED" . "output assert failed in $filename (line $line): $exp_out =/= $output" . $END . "\n";
    }

    $__DAGQL_TESTS_FAILED__ ||= !($output eq $exp_out) || 0;
}

assert_output('edges.dag',
q+359380 359379 
359384 31996 
359384 359389 
218451 218450 
+);

assert_output('shadow.dag',
q+218450 
359384 
31996 
359380 
+);

assert_output('limit.dag',
q+218451 
359384 
359380 
218450 
+);

exit $__DAGQL_TESTS_FAILED__;
