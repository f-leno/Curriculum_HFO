function generateGraphForExperiments(sourcePath,hfo)
% Function for displaying the experimental graphs
% sourcePath: Path for the experimental results (folders containing
% __SUMMARY files and etc.)
% hfo: Are the graphs for the HFO domain?

%Formats for printing (Color, marker)
formats = {{[166,97,26]/255,'o'},
           {[223,194,125]/255,'*'},
           {[128,205,193]/255,'d'},
           {[1,133,113]/255,'h'},
};

%Here, the name of folders and algorithms are defined
if hfo
    algorithms = {'SARSA-NoneCurriculum',
                  'PITAMSARSA-GeneratedSourceOOCurriculum',
                  'VFReuseSARSA-SvetlikCurriculum',
                  'PITAMSARSA-ObjectOrientedCurriculum'};
    names = {'No Curriculum','OO-Generated','Svetlik','OO-Given'};
    allGraphs = {'__SUMMARY_goal'};
end


%All graphs are here generated
for whatInd = 1:length(allGraphs)
    figure();
    hold all;
    controlIndex = 1;
    what = allGraphs{whatInd};
    for algIndex=1:length(algorithms)
        %Current Format
        alg = algorithms{algIndex};
        f = formats{controlIndex};
        
        [xValues,averages,errors] = readResultFile(sourcePath,alg,what);
        %Removes some of the error bars
        initialVal = xValues(1)/2000
        errors( find( mod( 1:(length(xValues)) , 3 ) ~= mod(initialVal+1,3) ) ) = NaN;
        
        h = errorbar(xValues,averages,errors,'Color',f{1})%,'Marker',f{2},'LineWidth',4);
        plot(xValues,averages,'Color',f{1},'Marker',f{2},'LineWidth',4)
        
        controlIndex = controlIndex + 1;
    end
end
                  



end

function [xValues, averages, errors] = readResultFile(sourcePath,alg,what) 
%Loads the result files and returns for the display function

fullPath = strcat(sourcePath,alg,'/',what);
data = csvread(fullPath,1);
xValues = data(:,1);
averages = data(:,2);
errors = data(:,4) - data(:,2);

end

