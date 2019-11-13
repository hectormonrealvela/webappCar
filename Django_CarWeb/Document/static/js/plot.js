$(document).ready(function(){


            var data_x = JSON.parse($("#xdata").attr("data"))

            var data_y = JSON.parse($("#ydata").attr("data"))

            var data_z = JSON.parse($("#zdata").attr("data"))

            var filename = $("#filename").attr("data");



            var trace1 = { x:data_x,
                           y:data_y,
                           z:data_z,
                          mode: "markers",
                          marker: {
                                   color: data_z,
                                   colorscale: 'Earth',
                                   size : 0.75,
                                   symbol: 'circle',

                                },
                                type: "scatter3d",
                          };


                          var data = [trace1];
                          var layout = {

                          width:950,
                          height:700,

                          scene: {

                                showlegend: false,
                                xaxis: {

                                     range: [-125, 125]

                                },
                                yaxis: {
                                    range: [-125, 125],

                                },
                                zaxis: {
                                    range: [-125, 125],
                                }

                          },
                          paper_bgcolor:'rgba(40,57,90,.8)',
                            };
                          Plotly.newPlot("myDiv", data, layout,);

                          var plotly_scatter_div = document.getElementById("myDiv");

                          plotly_scatter_div.on("plotly_click", function(data) {

                                var path = filename;

                                for(var i=0; i < data.points.length; i++){
                                                      var xquery=data.points[i].x ;
                                                      var yquery= data.points[i].y;
                                                      var zquery = data.points[i].z;

                                document.getElementById("myform").elements[3].value=path;
                                document.getElementById("myform").elements[4].value=xquery;
                                document.getElementById("myform").elements[5].value=yquery;
                                document.getElementById("myform").elements[6].value=zquery;


                                }

                          setTimeout(function(x) {

                            }, 50);

                          });

                     });