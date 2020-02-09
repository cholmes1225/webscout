#!/usr/bin/perl -w

use strict;
use warnings;

my $event = "";
my @red;
my @blue;

my $green = "#7ef542";

#
# read in given game data
#
if ($ENV{QUERY_STRING}) {
	my @args = split /\&/, $ENV{QUERY_STRING};
	my %params;
	foreach my $arg (@args) {
		my @bits = split /=/, $arg;
		next unless (@bits == 2);
		$params{$bits[0]} = $bits[1];
	}
	$event = $params{'event'}  if (defined $params{'event'});
	push @red, $params{'r1'} if (defined $params{'r1'});
	push @red, $params{'r2'} if (defined $params{'r2'});
	push @red, $params{'r3'} if (defined $params{'r3'});
	push @blue, $params{'b1'} if (defined $params{'b1'});
	push @blue, $params{'b2'} if (defined $params{'b2'});
	push @blue, $params{'b3'} if (defined $params{'b3'});
}

# print web page beginning
print "Content-type: text/html\n\n";
print "<html>\n";
print "<head>\n";
print "<title>FRC 1073 Scouting App</title>\n";
print "</head>\n";
print "<body bgcolor=\"#dddddd\"><center>\n";
print "<H1>Match Predictor</H1>\n";
print "<p><a href=\"index.cgi\">Home</a></p>\n";
if ($event eq "") {
    print "<H2>Error, need an event</H2>\n";
    print "</body></html>\n";
    exit 0;
}

#
# Load event data
#
my $file = "/var/www/html/csv/${event}.txt";
if (! -f $file) {
    print "<H2>Error, file $file does not exist</H2>\n";
    print "</body></html>\n";
    exit 0;
}

my %teamScore;
my %teamAuto;
my %teamTeleop;
my %teamCtrl;
my %teamEnd;
my %teamCount;
if ( open(my $fh, "<", $file) ) {
    while (my $line = <$fh>) {
	my @items = split /,/, $line;
	next if (@items < 6 || $items[0] eq "event");
	my $team = $items[2];
	my $ALin = int $items[3];
	my $ABot = int $items[4];
	my $AOut = int $items[5];
	my $AInn = int $items[6];
	my $TBot = int $items[7];
	my $TOut = int $items[8];
	my $TInn = int $items[9];
	my $RotC = int $items[36];
	my $PosC = int $items[37];
	my $park = int $items[38];
	my $clim = int $items[39];
	my $levl = int $items[42];
	$teamScore{$team}  = 0 unless (defined $teamScore{$team});
	$teamAuto{$team}   = 0 unless (defined $teamAuto{$team});
	$teamTeleop{$team} = 0 unless (defined $teamTeleop{$team});
	$teamCtrl{$team}   = 0 unless (defined $teamCtrl{$team});
	$teamEnd{$team}    = 0 unless (defined $teamEnd{$team});

	my $auto = ($ALin * 5) + ($ABot * 2) + ($AOut * 4) + ($AInn * 6);
	my $tele = $TBot + ($TOut * 2) + ($TInn * 3);
	my $ctrl = ($RotC * 10) + ($PosC * 20);
	my $endp = ($park * 5) + ($clim * 25) + ($levl * 15);
	$teamAuto{$team} += $auto;
	$teamTeleop{$team} += $tele;
	$teamCtrl{$team} += $ctrl;
	$teamEnd{$team} += $endp;

	$teamScore{$team} += $auto + $tele + $ctrl + $endp;
	
	if (defined $teamCount{$team}) {
	    $teamCount{$team} += 1;
	} else {
	    $teamCount{$team} = 1;
	}
    }
    close $fh;
} else {
    print "<H2>Error, could not open $file: $!</H2>\n";
    print "</body></html>\n";
    exit 0;
}

sub printTeam {
    my ($pos, $team) = (@_);
    print "<td>$pos</td><td>";
    if ($team ne "") {
        print "$team";
    } else {
        print "&nbsp;";
    }
    print "</td>\n";
}

# provide team selection if teams not given
if (@red != 3 || @blue != 3) {
    print "<FORM ACTION=\"matchup.cgi\">\n";
    print "<INPUT TYPE=\"hidden\" NAME=\"r1\" VALUE=\"$red[0]\">" if (@red > 0);
    print "<INPUT TYPE=\"hidden\" NAME=\"r2\" VALUE=\"$red[1]\">" if (@red > 1);
    print "<INPUT TYPE=\"hidden\" NAME=\"r3\" VALUE=\"$red[2]\">" if (@red > 2);
    print "<INPUT TYPE=\"hidden\" NAME=\"b1\" VALUE=\"$blue[0]\">" if (@blue > 0);
    print "<INPUT TYPE=\"hidden\" NAME=\"b2\" VALUE=\"$blue[1]\">" if (@blue > 1);
    print "<INPUT TYPE=\"hidden\" NAME=\"b3\" VALUE=\"$blue[2]\">" if (@blue > 2);

    print "<table cellpadding=5 cellspacing=5 border=1>\n";
    my $filler = "&nbsp;";
    $filler = $red[0] if (@red > 0);
    print "<tr><td>Red 1</td><td>$filler</td>\n";
    $filler = "&nbsp;";
    $filler = $blue[0] if (@blue > 0);
    print "<td>Blue 1</td><td>$filler</td></tr>\n";
    print "</tr><tr>\n";
    $filler = "&nbsp;";
    $filler = $red[1] if (@red > 1);
    print "<tr><td>Red 2</td><td>$filler</td>\n";
    $filler = "&nbsp;";
    $filler = $blue[1] if (@blue > 1);
    print "<td>Blue 2</td><td>$filler</td></tr>\n";
    print "</tr><tr>\n";
    $filler = "&nbsp;";
    $filler = $red[2] if (@red > 2);
    print "<tr><td>Red 3</td><td>$filler</td>\n";
    $filler = "&nbsp;";
    $filler = $blue[2] if (@blue > 2);
    print "<td>Blue 3</td><td>$filler</td></tr>\n";
    print "</tr></table>\n";

    my $pos = "Red 1";
    my $link = "matchup.cgi?event=${event}&r1=";
    if (@red == 1) {
        $pos = "Red 2";
	$link = "matchup.cgi?event=${event}&r1=$red[0]&r2=";
    }
    if (@red == 2) {
        $pos = "Red 3";
	$link = "matchup.cgi?event=${event}&r1=$red[0]&r2=$red[1]&r3=";
    }
    if (@red == 3) {
        $pos = "Blue 1";
	$link = "matchup.cgi?event=${event}&r1=$red[0]&r2=$red[1]&r3=$red[2]&b1=";
    }
    if (@blue == 1) {
        $pos = "Blue 2";
	$link = "matchup.cgi?event=${event}&r1=$red[0]&r2=$red[1]&r3=$red[2]&b1=$blue[0]&b2=";
    }
    if (@blue == 2) {
        $pos = "Blue 3";
	$link = "matchup.cgi?event=${event}&r1=$red[0]&r2=$red[1]&r3=$red[2]&b1=$blue[0]&b2=$blue[1]&b3=";
    }
    

    print "<H3>Select ${pos}:</H3>\n";
    my @teams = sort(keys %teamScore);
    print "<table cellpadding=5 cellspacing=5 border=1><tr>\n";
    my $count = 0;
    foreach my $t (@teams) {
    	my $found = 0;
	foreach my $c (@red, @blue) {
		if ($c eq $t) {
			$found = 1;
			last;
		}
	}
	next if ($found != 0);
        print "<td><a href=\"${link}$t\">$t</a></td>\n";
	$count++;
	print "</tr><tr>\n" if ($count % 7 == 0);
    }
    while ($count % 7 != 0) {
    	$count++;
	print "<td>&nbsp;</td>\n";
    }
    print "</tr></table>\n";
    print "</body></html>\n";
    exit 0;
}

# RED
print "<table cellpadding=2 cellspacing=2 border=1>\n";
print "<tr><th colspan=7><p style=\"font-size:25px; font-weight:bold;\">Red Alliance</p></th></tr>\n";
print "<tr><th>Team</TH><TH># Matches</TH><th>OPR</TH>";
print "<TH>Avg. Auto Score</TH><TH>Avg. TeleOp Score</TH>";
print "<TH>Avg Ctrl Score</TH><TH>Avg End Game</TH></tr>\n";

# gather red high scores
my $hopr  = 0;
my $hauto = 0;
my $htele = 0;
my $hctrl = 0;
my $hend  = 0;
for (my $i = 0; $i < 3; $i++) {
    my $opr  = $teamScore{$red[$i]} / $teamCount{$red[$i]};
    my $auto = $teamAuto{$red[$i]} / $teamCount{$red[$i]};
    my $tele = $teamTeleop{$red[$i]} / $teamCount{$red[$i]};
    my $ctrl = $teamCtrl{$red[$i]} / $teamCount{$red[$i]};
    my $endp = $teamEnd{$red[$i]} / $teamCount{$red[$i]};
    $hopr  = $opr  if ($opr > $hopr);
    $hauto = $auto if ($auto > $hauto);
    $htele = $tele if ($tele > $htele);
    $hctrl = $ctrl if ($ctrl > $hctrl);
    $hend  = $endp if ($endp > $hend);
}

my $redtotal = 0;
for (my $i = 0; $i < 3; $i++) {
    my $opr  = $teamScore{$red[$i]} / $teamCount{$red[$i]};
    my $auto = $teamAuto{$red[$i]} / $teamCount{$red[$i]};
    my $tele = $teamTeleop{$red[$i]} / $teamCount{$red[$i]};
    my $ctrl = $teamCtrl{$red[$i]} / $teamCount{$red[$i]};
    my $endp = $teamEnd{$red[$i]} / $teamCount{$red[$i]};

    $redtotal += $opr;

    my $ostr = sprintf "%.3f", $opr;
    my $astr = sprintf "%.3f", $auto;
    my $tstr = sprintf "%.3f", $tele;
    my $cstr = sprintf "%.3f", $ctrl;
    my $estr = sprintf "%.3f", $endp;

    print "<tr><td><p style=\"font-size:25px; font-weight:bold;\">";
    print "<a href=\"team.cgi?team=$red[$i]&event=$event\">$red[$i]</a></p></td>";
    print "<td><p style=\"font-size:25px; font-weight:bold;\">$teamCount{$red[$i]}</p></td>\n";

	my $bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hopr == $opr);
	print "<td $bgcolor><p style=\"font-size:25px; font-weight:bold;\">$ostr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hauto == $auto);
    print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$astr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($htele == $tele);
    print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$tstr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hctrl == $ctrl);
    print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$cstr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hend == $endp);
    print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$estr</p></td></tr>";
}
print "</table>\n";

# BLUE
print "<table cellpadding=2 cellspacing=2 border=1>\n";
print "<tr><th colspan=7><p style=\"font-size:25px; font-weight:bold;\">Blue Alliance</p></th></tr>\n";
print "<tr><th>Team</TH><TH># Matches</TH><th>OPR</TH>";
print "<TH>Avg. Auto Score</TH><TH>Avg. TeleOp Score</TH>";
print "<TH>Avg Ctrl Score</TH><TH>Avg End game</TH></tr>\n";

# gather blue high scores
$hopr  = 0;
$hauto = 0;
$htele = 0;
$hctrl = 0;
$hend  = 0;
for (my $i = 0; $i < 3; $i++) {
    my $opr  = $teamScore{$blue[$i]} / $teamCount{$blue[$i]};
    my $auto = $teamAuto{$blue[$i]} / $teamCount{$blue[$i]};
    my $tele = $teamTeleop{$blue[$i]} / $teamCount{$blue[$i]};
    my $ctrl = $teamCtrl{$blue[$i]} / $teamCount{$blue[$i]};
    my $endp = $teamEnd{$blue[$i]} / $teamCount{$blue[$i]};
	$hopr  = $opr  if ($opr > $hopr);
	$hauto = $auto if ($auto > $hauto);
	$htele = $tele if ($tele > $htele);
	$hctrl = $ctrl if ($ctrl > $hctrl);
	$hend  = $endp if ($endp > $hend);
}

my $bluetotal = 0;
for (my $i = 0; $i < 3; $i++) {
	my $opr  = $teamScore{$blue[$i]} / $teamCount{$blue[$i]};
	my $auto = $teamAuto{$blue[$i]} / $teamCount{$blue[$i]};
	my $tele = $teamTeleop{$blue[$i]} / $teamCount{$blue[$i]};
	my $ctrl = $teamCtrl{$blue[$i]} / $teamCount{$blue[$i]};
	my $endp = $teamEnd{$blue[$i]} / $teamCount{$blue[$i]};

	$bluetotal += $opr;
	my $ostr = sprintf "%.3f", $opr;
	my $astr = sprintf "%.3f", $auto;
	my $tstr = sprintf "%.3f", $tele;
	my $cstr = sprintf "%.3f", $ctrl;
	my $estr = sprintf "%.3f", $endp;
	
	print "<tr><td><p style=\"font-size:25px; font-weight:bold;\">";
	print "<a href=\"team.cgi?team=$blue[$i]&event=$event\">$blue[$i]</a></p></td>";
	print "<td><p style=\"font-size:25px; font-weight:bold;\">$teamCount{$blue[$i]}</p></td>\n";

	my $bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hopr == $opr);
	print "<td $bgcolor><p style=\"font-size:25px; font-weight:bold;\">$ostr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hauto == $auto);
	print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$astr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($htele == $tele);
	print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$tstr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hctrl == $ctrl);
	print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$cstr</p></td>";
	$bgcolor="";
	$bgcolor="bgcolor=\"$green\"" if ($hend == $endp);
	print "<td $bgcolor><p style=\"font-size:20px; font-weight:bold;\">$estr</p></td></tr>\n";
}
print "</table>\n";

my $rt = sprintf "%.1f", $redtotal;
my $bt = sprintf "%.1f", $bluetotal;
print "<H2>Red Alliance Score: $rt</H2>\n";
print "<H2>Blue Alliance Score: $bt</H2>\n";

print "</body></html>\n";
