function greenchip_plotter(outfile)

    M = csvread(outfile);
    val2d_alt = (reshape(M(:,3),[101, 100]));
	val2d_alt(val2d_alt<0)=100*365;
    mappy = zeros(101,3);
    %RED
    mappy(1:13, 1) = linspace(0, 1, 13-1+1);
    mappy(14:26, 1) = linspace(1, 0, 26-14+1);
    mappy(53:65, 1) = linspace(0, 1, 65-53+1);
    mappy(66:90, 1) = 1;
    mappy(91:101, 1) = linspace(1, 0.3, 101-91+1);
    %GREEN
    mappy(27:39,2) = linspace(0,0.5,39-27+1);
    mappy(40:52,2) = linspace(0.5,1,52-40+1);
    mappy(53:65, 2) = 1;
    mappy(66:78,2) = linspace(1,0.5,78-66+1);
    mappy(79:90,2) = linspace(0.5,0,90-79+1);
    mappy(91:101,2) = linspace(0,0.3,101-91+1);
    %BLUE
    mappy(1:13, 3) = linspace(0, 1, 13-1+1);
    mappy(14:26,3)=1;
    mappy(27:39,3) = linspace(1,0.5,39-27+1);
    mappy(40:52,3) = linspace(0.5,0,52-40+1);
    mappy(91:101,3) = linspace(0,0.3,101-91+1);

    figure
    colormap(mappy);
    imagesc(val2d_alt)
    colorbar
    caxis([0 3650])

    ylabel(colorbar, 'Days');
    ylabel('Active Ratio');
    xlabel( 'Sleep Ratio');

end
