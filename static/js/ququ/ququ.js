
class QUQU {
    constructor(propertyDict) {
        if(propertyDict.container == undefined) {
            this.width = window.innerWidth;
            this.height = window.innerHeight;

            this.svg = d3.select("body").append("svg");
        } else {
            this.width = propertyDict.container.width();
            this.height = propertyDict.container.height();
            this.width = this.width+this.width*0.4;
            this.height = this.height + this.height*0.03;
            this.propDic = propertyDict.container[0].id;
            this.svg = d3.select("#"+propertyDict.container[0].id)
                .append("svg")
                .attr("viewBox", "0 0 " + (this.width-10).toString() + " " + (this.height-10).toString())
                .attr("preserveAspectRatio", "xMidYMid meet")
                .classed("svg-content-responsive", true);

        }

        this.svg.append("rect")
            .attr("x", 0)
            .attr("y", 0) 
            .attr("viewBox", "0 0 " + this.width + " " + this.height)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .style("stroke", "black")
            .style("fill", "none")
            .style("stroke-width", 2)
            .classed("svg-container", true)
            .classed("svg-content-responsive", true);

        this.cursor = this.svg.append("circle")
            .attr("r", 0)
            .attr("transform", "translate(-100,-100)")
            .attr("class", "cursor");

        this.max_radius = 2500;
        this.min_radius = 500;
        this.avg_img_radius = 0;
        this.min_img_radius = 99999;
        this.max_img_radius = 0;
        this.max_link_distance = 0;
        this.max_link_count = 0;
        this.max_inlinks = 0;
        this.min_link_count = 0;
        this.link_total = 0;
        this.node_total = 0;
        this.number_of_constants = 0;
        this.node = null;
        this.link = null;
        this.labels = null;
        this.images = null;
        this.marker = null;
        this.simulation = null;
        this.charge_force = null;
        this.link_force = null;
        this.collide_force = null;
        this.xforce = null;
        this.yforce = null;
        this.center_force = null;
        this.g = null;
        this.zoom_handler;

        this.zoomcount = 0;

        this.search_value = null;

        this.NRL = new Map();

        this.img_w = 0;
        this.img_offset = 0;

        this.delete_mode = 0;
        this.hide_mode = 0;


        this.user_json = propertyDict.uploaded_json;
        this.nodes_data = this.user_json['nodes_data'];
        this.links_data = this.user_json['links_data'];

        this.deleted_nodes = new Map();
        this.deleted_links = new Map();
        if(this.user_json['max_area']) {
            this.max_img_area = this.user_json['max_area'];
        }
        //console.log(this.user_json);

        this.initGraph();
        //this.mathJaxLatex(propertyDict);

    }

    /** Functions **/

    redefine_class_variables() {
        this.max_radius = 2500;
        this.min_radius = 500;
        this.avg_img_radius = 0;
        this.min_img_radius = 99999;
        this.max_img_radius = 0;
        this.max_link_distance = 0;
        this.max_link_count = 0;
        this.max_inlinks = 0;
        this.min_link_count = 0;
        this.link_total = 0;
        this.node_total = 0;
        this.number_of_constants = 0;
        this.node = null;
        this.link = null;
        this.labels = null;
        this.images = null;
        this.marker = null;
        this.simulation = null;
        this.charge_force = null;
        this.link_force = null;
        this.collide_force = null;
        this.xforce = null;
        this.yforce = null;
        this.center_force = null;
        this.g = null;
        this.zoom_handler;
        this.autozoom = null;

        this.search_value = null;

        this.NRL = new Map();

        this.img_w = 0;
        this.img_offset = 0;
    }

    re_calc_inout_links(quqn) {
        quqn.nodes_data.forEach(function(d,i) {
            var inlink_count = 0;
            var outlink_count = 0;
            quqn.links_data.forEach(function(l,k) {
                if(l.source.name == d.name) {
                    outlink_count = outlink_count + 1
                }
                if(l.target.name == d.name) {
                    inlink_count = inlink_count + 1
                }
            });
            d.inlinks = inlink_count;
            d.outlinks = outlink_count;
        });
    }

    node_radius_by_img_length(d, quqn) {
        var radius = quqn.avg_img_radius;
        radius = radius + ((parseInt(d.inlinks))*quqn.min_radius) + quqn.min_radius;
        /*if(parseInt(d.inlinks) >= 1){
            radius = radius * parseInt(d.inlinks) + quqn.min_radius;
            if(radius > quqn.max_radius) {
                radius = quqn.max_radius;
            }
        } else {
            radius = quqn.min_radius;
        }
        var link_ratio = 0;
        if(parseInt(d.inlinks) > parseInt(d.outlinks)) {
            var denom= parseInt(d.outlinks);
            if(denom == 0) { denom = 1;}
            link_ratio = (parseInt(d.inlinks)) / (denom);
        } else {
            var denom= parseInt(d.inlinks);
            if(denom == 0) { denom = 1;}
            link_ratio = (parseInt(d.outlinks)) / (denom);
        }

        var radius = link_ratio * d.img_size[0] + quqn.min_radius;
        */
        if(radius > quqn.max_radius) {
            radius = quqn.max_radius;
        }
        
        if(!quqn.NRL.get(d.name)) {
            quqn.NRL.set(d.name, radius);
        }
        return radius;
        console.log(radius);
    }

    mousemove(cursor, var_xy) {
        cursor.attr('transform', 'translate(' + var_xy[0] + "," + var_xy[1] + ')');
    }

    find_nearest_node(cursor_point) {
        // Mouse left click
        var local_quqn = this;
        var nearest_node = -1;
        var nearest_distance = -1;
        local_quqn.node.attr("cx", function(d,i) {

            //console.log("WTF");
            var x = d.x - cursor_point[0];
            var y = d.y - cursor_point[1];
            var nn_distance = Math.sqrt(x*x + y*y);
            if(nn_distance < 35)
            {
                if(nearest_node == -1 || nn_distance < nearest_distance)
                {
                    nearest_node = d;
                    nearest_distance = nn_distance;                         
                }
            }
        });     

        return nearest_node;
    }

    delete_candidate(d) {
        this.node.style("fill", function(l) {
            if(l.name == d.name) {
                d.D = "1";
                return "red";
            } else {
                return "white";
            }
        });
        this.links_data.forEach(function(l,i) {
            if(l.target.name == d.name || l.source.name == d.name) {
                l.D = "1";
            }
        });
    }

    undelete_candidate(d) {
        this.node.style("fill-opacity", function(l) {
            if(l.name == d.name) {
                l.D = "0";
                return 1;
            } else {
                if(l.D == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.links_data.forEach(function(l,i) {
            if(l.target.name == d.name || l.source.name == d.name) {
                l.D = "0";
            }
        });
    }

   unhide_candidate(d) {
        this.node.style("fill-opacity", function(l) {
            if(l.name == d.name) {
                l.H = "0";
                return 1;
            } else {
                if(l.H == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.node.style("stroke-opacity", function(l) {
            if(l.name == d.name) {
                l.H = "0";
                return 0.2;
            } else {
                if(l.H == "0") {
                    return 0.2;
                } else {
                    return 0;
                }
            }
        });
        this.images.style("opacity", function(l) {
            if(l.name == d.name) {
                l.H = "0";
                return 1;
            } else {
                if(l.H == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.labels.style("fill-opacity", function(l) {
            if(l.name == d.name) {
                l.H = "0";
                return 1;
            } else {
                if(l.H == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.link.style("stroke-opacity", function(l) {
            if(l.source.name == d.name || l.target.name == d.name) {
                l.H = "0";
                return 0.6;
            } else {
                if(l.H == "0") {
                    return 0.6;
                } else {
                    return 0;
                }
            }
        });

        this.charge_force.strength(function(n) {
            if(n.name == d.name) {
                return -700000; 
           } else {
                if(n.H == "0") {
                    return -700000;
                } else {
                    return 0; 
                }
                
           }
            
        });

        this.simulation.alpha(0.3).restart();   
   }
   hide_candidate(d) {
        this.node.style("fill-opacity", function(l) {
            if(l.name == d.name) {
                l.H = "1";
                return 0;
            } else {
                if(l.H == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.node.style("stroke-opacity", function(l) {
            if(l.name == d.name) {
                l.H = "1";
                return 0;
            } else {
                if(l.H == "0") {
                    return 0.2;
                } else {
                    return 0;
                }
            }
        });
        this.images.style("opacity", function(l) {
            if(l.name == d.name) {
                l.H = "1";
                return 0;
            } else {
                if(l.H == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.labels.style("fill-opacity", function(l) {
            if(l.name == d.name) {
                l.H = "1";
                return 0;
            } else {
                if(l.H == "0") {
                    return 1;
                } else {
                    return 0;
                }
            }
        });
        this.link.style("stroke-opacity", function(l) {
            if(l.source.name == d.name || l.target.name == d.name) {
                l.H = "1";
                return 0;
            } else {
                if(l.H == "0") {
                    return 0.6;
                } else {
                    return 0;
                }
            }
        });
        this.marker.style("fill-opacity", function(l) {
            if(l.target.name == d.name) {
                return 0;
            } else {
                return 0.8;
            }       
        });

        this.charge_force.strength(function(n) {
            if(n.name != d.name) {
                return -700000; 
           } else {
                return 0;
           }
            
        });

        this.simulation.alpha(0.3).restart();
    }

    // Node color
    circleColour(inlinks, outlinks){
        var total = parseInt(inlinks) + parseInt(outlinks);
        if(total == parseInt(inlinks) || (parseInt(inlinks) == 3 && parseInt(outlinks) == 1) || (parseInt(inlinks) == 5 && parseInt(outlinks) == 1)) {
            if(total == 2 || total == 1) {
                return "#D8BFD8";
            } else {
                return "#FCA4EA";    
            }
            
        } else if(total == parseInt(outlinks) || (parseInt(inlinks) == 2 && parseInt(outlinks) == 5)) {
            return "#C0C0C0";
        } else {
            return "white"
        }
    }

    download_map(quqn) {
        var new_map = {}
        new_map["nodes_data"] = quqn.nodes_data;
        new_map["links_data"] = quqn.links_data;
        return new_map;
    }

    //Set delete flag to zero
    deleteFlag(val, qn) {
        qn.delete_mode = val;
        if(val == 0) {
            qn.node.style("fill", function(d) {
                d.D = "0";
                return qn.circleColour(parseInt(d.inlinks), parseInt(d.outlinks));
            });
            qn.links_data.forEach(function(l,i) {
                l.D = "0";
            });
        }
    }

    hideFlag(val, qn) {
        qn.hide_mode = val;
    }

    delete_node(quqn, jdata) {
        if(this.delete_mode == "1") {

            for(var i = quqn.links_data.length - 1; i >= 0; i--) {
                if(quqn.links_data[i].D == "1") {
                    quqn.links_data.splice(i,1);
                } 
            }
            for(var i = quqn.nodes_data.length - 1; i >= 0; i--) {
                if(quqn.nodes_data[i].D == "1") {
                    quqn.nodes_data.splice(i,1);
                }
            }

            quqn.re_calc_inout_links(quqn);
            d3.select("svg").remove();
            quqn.svg = d3.select("#"+quqn.propDic)
                .append("svg")
                .style("width", this.width-10)
                .style("height", this.height-10);
            quqn.svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("height", this.height)
                .attr("width", this.width)
                .style("stroke", "black")
                .style("fill", "none")
                .style("stroke-width", 2);
            quqn.redefine_class_variables();
            quqn.initGraph();
        } 
        //console.log(quqn.nodes_data)
    }

    //Function to choose the line colour
    linkColour(link_type){
        if(link_type == "A"){
            return "green";
        } else {
            return "black";
        }
    }

    //Drag functions 
    //d is the node 
    drag_start(d) {
        if (!d3.event.active) this.simulation.alphaTarget(0.01).restart();
        d.fx = d.x;
        d.fy = d.y;
        if(this.delete_mode == 1) {
            if(d.D == "0") {
                this.delete_candidate(d);    
            } else {
                this.undelete_candidate(d);
            }
            
        }  
        if(this.hide_mode == 1) {
            if(d.H == "0") {
                this.hide_candidate(d); 
           } else {
                this.unhide_candidate(d);
           }
            
        }
        get_node_page(parseInt(d.P[0]));
        return d;
    }

    //make sure you can't drag the circle outside the box
    drag_drag(d, new_d, cursor) {
        d.fx = new_d.x;
        d.fy = new_d.y;
        //cursor.attr('transform', 'translate(' + d.fx + "," + d.fy + ')');
        return d;
    }

    // Freez the node at end position
    drag_end(d) {
        if (!d3.event.active) this.simulation.alphaTarget(0);
        d.fx = d.x;
        d.fy = d.y;
        return d;
    }

    //Zoom functions 
    zoom_actions(var_g){
        //console.log(d3.event.transform);
        var_g.attr("transform", d3.event.transform);

        //var_g.attr("transform", d3.event.transform);
        //var_g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }

    tickActions() {
        //update circle positions each tick of the simulation 
        var local_quqn = this;
        if(local_quqn.node != undefined) {
            var const_id = 0;
            var const_yid = 0;
            local_quqn.node
                .attr("cx", function(d) {
                    return d.x; 
                })
                .attr("cy", function(d) { 
                    //return d.y = Math.max(15, Math.min((local_quqn.height + local_quqn.height), d.y))
                    //d.y = -local_quqn.height + (-1^const_yid * 100);
                    //const_yid = const_yid + 1
                    //console.log(d.P);
                    return d.y;     
                });

            //update link positions and marker positions
            if(local_quqn.link != undefined) {
                local_quqn.link
                    .attr("x1", function(d) {
                        var dx = d.source.x;
                        return dx; 
                    })
                    .attr("y1", function(d) { 
                        var dy = d.source.y;
                        return dy; 
                    })
                    .attr("x2", function(d) { return d.target.x; })
                    .attr("y2", function(d) { return d.target.y; });
            }

            //Update node labels
            if(local_quqn.link != undefined) {
                local_quqn.labels
                    .attr("x", function(d) { 
                        var radius = local_quqn.node_radius_by_img_length(d, local_quqn)
                        return d.x + radius+53;
                    })
                    .attr("y", function(d) { return d.y;});
            }

            //Update Node images
            if(local_quqn.images != undefined) {
                local_quqn.images
                    .attr("x", function(d) { 
                        var radius = local_quqn.node_radius_by_img_length(d, local_quqn);
                        return  d.x - radius/2 - d.img_offset;
                    })
                    .attr("y", function(d) { 
                        var radius = local_quqn.node_radius_by_img_length(d, local_quqn);
                        return  d.y - radius/2 - d.img_offset;
                    });
            }

        }
    } 

    initGraph() {
        var quqn = this;
        /*
            Get max link distance and other node props. Will be done in python latter
            and passed in with jason data
        */
        quqn.nodes_data.forEach(function(d) {
            /*console.log(d.P);
            console.log(d.C);
            console.log(d.decleration);*/
            if(d.constant == "1"){
                quqn.number_of_constants = quqn.number_of_constants + 1
            }
            quqn.node_total = quqn.node_total + 1;

            var total_links = parseInt(d.inlinks);
            quqn.link_total = quqn.link_total + total_links;
            if(total_links > quqn.max_link_distance) {
                quqn.max_link_distance = total_links;
            }
            if(quqn.min_link_count == 0) {
                quqn.min_link_count = total_links;
            } else {
                if(quqn.min_link_count > total_links) {
                    quqn.min_link_count = total_links
                }
            }
            if(quqn.max_link_count == 0) {
                quqn.max_link_count = total_links;
            } else {
                if(quqn.max_link_count < total_links) {
                    quqn.max_link_count = total_links;
                }
            }

            //img data
            d.img_radius = Math.sqrt(Math.pow(parseInt(d.img_size[0]),2), Math.pow(parseInt(d.img_size[1]),2));
            quqn.avg_img_radius = quqn.avg_img_radius + d.img_radius;
            if(d.img_radius > quqn.max_img_radius) {
                quqn.max_img_radius = d.img_radius;
            }
            if(d.img_radius < quqn.min_img_radius) {
                quqn.min_img_radius = d.img_radius;
            }
            return d;
        });

        quqn.avg_img_radius = quqn.avg_img_radius / quqn.node_total;
        //console.log(quqn.min_img_radius);
        // Normalize forces for small graphs, 0.15 is expperimental
        /*if(quqn.max_link_distance / quqn.link_total > 0.15) {
            quqn.link_total = quqn.link_total * 10 * ((quqn.max_link_distance / quqn.link_total)/0.15);
        }*/

        quqn.svg.on('mousemove', function() {
            quqn.mousemove(quqn.cursor, d3.mouse(document.getElementById("quqn_window")));
        });

        /*quqn.svg.on('click', function() {
        });*/

        /*quqn.svg.on('mousedown', function() {
            var nn = quqn.find_nearest_node(d3.mouse(document.getElementById("quqn_window")));
            console.log("wtf");
            console.log(nn);
            d3.mouse(document.getElementById("quqn_window"))[0] = nn.x;
            d3.mouse(document.getElementById("quqn_window"))[1] = nn.y;
            if(quqn.delete_mode == 1) {
                //this.deleted_nodes = new Map();
                //this.deleted_links = new Map();
            }
        });*/

        quqn.simulation = d3.forceSimulation()
                        .nodes(quqn.nodes_data);
                                  
        quqn.link_force =  d3.forceLink(quqn.links_data)
                                .id(function(d) { 
                                    return d.name; 
                                })
                                .distance(function(d, i) { 
                                    var link_distance = 0;
                                    var radius = 0
                                    // Turn to hash latter
                                    quqn.nodes_data.forEach(function(n) {
                                        if( n.name == d.source.name ) {
                                            var link_count = parseInt(n.inlinks) + parseInt(n.outlinks);
                                            if(Number(link_distance) < Number(link_count)) {
                                                link_distance = link_count;
                                                radius = quqn.node_radius_by_img_length(n, quqn);
                                            }
                                        } else if( n.name == d.target.name) {
                                            var link_count = parseInt(n.inlinks) + parseInt(n.outlinks) ;
                                            if(Number(link_distance) < Number(link_count)) {
                                                link_distance = link_count;
                                                radius = quqn.node_radius_by_img_length(n, quqn);
                                            }                                       
                                        }
                                    });
                                    //console.log(link_distance*radius);
                                    link_distance = link_distance*radius;
                                    if(link_distance > 5000) {
                                        return 5000;
                                    }
                                    return link_distance;
                                })
                                .strength(function(d) { 
                                    var link_distance = 0;
                                    var radius = 0;
                                    var link_charge = 0;
                                    // Turn to hash latter
                                    quqn.nodes_data.forEach(function(n) {
                                        if( n.name == d.source.name ) {
                                            var link_count =  parseInt(n.inlinks);
                                            if(Number(link_distance) < Number(link_count)) {
                                                link_distance = link_count;
                                                radius = quqn.node_radius_by_img_length(n, quqn);
                                            }
                                        } else if( n.name == d.target.name) {
                                            var link_count =  parseInt(n.outlinks);
                                            if(Number(link_distance) < Number(link_count)) {
                                                link_distance = link_count;
                                                radius = quqn.node_radius_by_img_length(n, quqn);
                                            }                                       
                                        }
                                        link_charge = (link_distance/quqn.max_link_distance);
                                        if(link_distance == 1) {
                                            link_charge = 0.1;
                                        }
                                    });
                                    //return link_distance/quqn.max_link_distance * 0.00001; 
                                    return 0.3;
                                });        
                 
        quqn.charge_force = d3.forceManyBody()
            // Try number of nodes times number of links
            //-(800000)
            .strength(function(d) {
                var radius = quqn.node_radius_by_img_length(d, quqn);
                /*if(d.inlinks > 10) {
                    return radius * 500;
                }*/
                /*if(d.inlinks == "0") {
                    return -parseInt(d.outlinks*3000);
                } else if(d.outlinks == "0") {
                    return -parseInt(d.inlinks)*3000;
                } else {
                    return -3000 * Math.abs(parseInt(d.inlinks)-parseInt(d.outlinks))
                }*/

                return -700000;
                
            });
            
        quqn.center_force = d3.forceCenter(quqn.width / 2, quqn.height / 2);  
                  
        quqn.collide_force = d3.forceCollide().radius(function(d) { 
                return quqn.node_radius_by_img_length(d, quqn)*2;
        }).iterations(2);

        var const_xid = -1;
        var const_yid = -1;
        /*quqn.xforce = d3.forceX().x(function(d) {
                if(d.inlinks > 0.75*quqn.total_links) {
                    return quqn.width / 2;
                }
            });

        quqn.yforce = d3.forceY().y(function(d) {
                if(d.inlinks > 0.75*quqn.total_links) {
                    return quqn.height / 2 ;
                }
            });*/

        quqn.simulation
            .force("charge_force", quqn.charge_force)
            .force("charge_center", quqn.center_force)
            .force("collide", quqn.collide_force)
            //.force("x", quqn.xforce)
            //.force("y", quqn.yforce)
            .force("links", quqn.link_force);

        //add encompassing group for the zoom 
        quqn.g = quqn.svg.append("g");

        quqn.g.append("filter")
            .attr("id", "glow")
            .append("feGaussianBlur")
            .attr("stdDeviation", "5")
            .attr("result", "coloredBlur");

        //draw lines for the links 
        quqn.link = quqn.g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(quqn.links_data)
            .enter().append("line")
            .attr("stroke-width", 15)
            .style("stroke-opacity", 0.6)
            .style("stroke", function(d) {
               return quqn.linkColour(d.type); 
            }).attr("marker-end", function(d) {
                return "url(#marker_" + d.target.name + ")";
            });

        //draw circles for the nodes 
        quqn.node = quqn.g.append("g")
            .attr("class", "nodes") 
            .selectAll("circle")
            .data(quqn.nodes_data)
            .enter()
            .append("circle")
            .attr("r", function(d) {
                //console.log(d);
                var radius = quqn.node_radius_by_img_length(d, quqn);
                return radius;
            })
            .style("fill-opacity", 1.0)
            .style("fill", function(d) {return quqn.circleColour(parseInt(d.inlinks), parseInt(d.outlinks));})
            .style("stroke-width", 10)
            .style("stroke-opacity", 0.2)
            .style("stroke", "black");

        //Arrow markers
        quqn.marker = quqn.g.append("g")
            .attr("class", "links")
            .selectAll("marker")
            //.data(["end"])
            .data(quqn.links_data)
            .enter()
            .append("svg:marker")
            .attr("id", function(d) {
                return "marker_" + d.target.name;
            })
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", function(d) {
                var radius = quqn.NRL.get(d.target.name);   
                var refx = 0
                if(radius == quqn.min_radius) {
                    refx = 30;
                } else {
                    // 0.039 = 108-30/2000 --> 2000 = max-min radius
                    // 30 is for 500 and 108 is for 2500 radius
                    refx = 30 + ((radius-quqn.min_radius) * 0.039);
                }
                return refx;
            })
            .attr("fill", "gray")
            .style("fill-opacity", 0.8)
            .attr("refY", 0)
            .attr("markerWidth", 17)
            .attr("markerHeight", 17)
            .attr("orient", "auto")
            .append("svg:path")
            .attr("d", "M0,-5L10,0L0,5");

        // Label text by the node
        quqn.labels = quqn.g.append("g")
            .attr("class", "nodes")
            .selectAll("text")
            .data(quqn.nodes_data)
            .enter()
            .append("text")
            .text(function(d) {
                    return d.decleration;
            })
            .attr('dx', 20)
            .style("fill", "black")
            .style("fill-opacity", 0.8)
            .style("font-size", function(d) {
                var text_size = quqn.node_radius_by_img_length(d, quqn)/2;
                if(text_size < 350) {
                    text_size = 350;
                }
                if(text_size > 600) {
                    text_size = 600;
                }
                return text_size;
            })
            .attr('dy', 3);

        quqn.node.append("title")
            .html(function(d) { 
                if(quqn.user_json == null) {
                    //return d.name;
                    return d.decleration;
                } else {
                    return d.decleration;
                }
                
            });

        

        quqn.node.on("mouseover", function(d) {
            quqn.on_hover_highlight_neighbors(d);
        });

        quqn.node.on("mouseout", function(d) {
            quqn.on_hover_out_unlight_neighbors(d);
        });

        // Image
        quqn.images = quqn.g.append("g")
            .attr("class", "nodes")
            .selectAll("image")
            .data(quqn.nodes_data)
            .enter()
            .append("svg:image")
            .attr("xlink:href", function(d) {
                return d.img;
            })
            .attr("x", function(d) {
                var radius = quqn.node_radius_by_img_length(d, quqn);
                return -radius; 
            })
            .attr("y", function(d) {
                var radius = quqn.node_radius_by_img_length(d, quqn);
                return -radius;
            }).attr("width", function(d) {
                var radius = quqn.node_radius_by_img_length(d, quqn);
                if(d.img_radius < 200) {
                    d.img_offset = radius/4;
                    return radius + radius/2;
                } else {
                    d.img_offset = radius/2;
                    return radius + radius;
                }   
            })
            .attr("height", function(d) {
                var radius = quqn.node_radius_by_img_length(d, quqn);
                if(d.img_radius < 200) {
                    d.img_offset = radius/4;
                    return radius + radius/2;
                } else {
                    d.img_offset = radius/2;
                    return radius + radius;
                }
            })
            .style("opacity", 1);

        quqn.images.append("title")
            .html(function(d) {
                //return "<image href=\"" + d.img + "\">";
                return d.decleration;
            });

        quqn.images.on("mouseover", function(d) {
            quqn.on_hover_highlight_neighbors(d);
        });

        quqn.images.on("mouseout", function(d) {
            quqn.on_hover_out_unlight_neighbors(d);
        })

        //add drag capabilities  
        var drag_handler = d3.drag()      
            .on("start", function(d) {
                return quqn.drag_start(d);
            })
            .on("drag", function(d) {
                return quqn.drag_drag(d, d3.event, quqn.cursor);
            })
            .on("end", function(d) {
                return quqn.drag_end(d); 
            });

        var drag_handler2 = d3.drag()
            .on("start", function(d) {
                //console.log(d);
                return quqn.drag_start(d);
            })
            .on("drag", function(d) {
                return quqn.drag_drag(d, d3.event, quqn.cursor);
            })
            .on("end", function(d) {
                return quqn.drag_end(d); 
            });

        drag_handler(quqn.node);
        drag_handler2(quqn.images);


        quqn.zoom_handler = d3.zoom()
            .on("zoom", function() {
                quqn.zoom_actions(quqn.g);
            });
        quqn.zoomFit(quqn);
        quqn.zoom_handler(quqn.svg);

        //add tick instructions:
        quqn.simulation.on("tick", function() {
            quqn.tickActions();
        });

        
    } 


    //Auto scale Zoom on load
    zoomFit(quqn) {
        //Center the graph and zoom out
        var bounds = quqn.g.node().getBBox();
        var parent = quqn.g.node().parentElement;

        var fullWidth = parent.clientWidth || parent.parentNode.clientWidth;
        var fullHeight = parent.clientHeight || parent.parentNode.clientHeight;

        var width = bounds.width;
        var height = bounds.height;


        var midX = bounds.x + width/2;
        var midY = bounds.y + height/2;
        if(width == 0 || height == 0) return;
        var scale = 0.5/Math.max(width / fullWidth, height/fullHeight);
        var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY]

        quqn.svg.transition()
            .call(quqn.zoom_handler.transform, d3.zoomIdentity.translate(translate[0],translate[1]).scale(scale));
    }

    //Search node by Name 
    searchBar(searchValue) {
        this.search_value = searchValue;
        var local_quqn = this;
        local_quqn.node.style("fill", function(d) {
            if(d.name != undefined) {
                if(searchValue != "") {
                    if(d.decleration.toLowerCase().includes(searchValue.toLowerCase())) {
                        return "#4EFC68";   
                    } else {
                        return local_quqn.circleColour(parseInt(d.inlinks), parseInt(d.outlinks));
                    }
                } else {
                    return local_quqn.circleColour(parseInt(d.inlinks), parseInt(d.outlinks));
                }
            }
        });
    }

    on_hover_highlight_neighbors(d) {
        var local_quqn = this;
        var node_list = new Object();
        local_quqn.link.style("stroke", function(l) {
            if(l.source.name == d.name || l.target.name == d.name) {
                node_list[l.source.name] = 1;
                node_list[l.target.name] = 1;
                return "#33F0FF";
            } //else {
             //   return "white";
            //}
        });
        local_quqn.link.style("stroke-opacity", function(l) {
            if((l.source.name == d.name || l.target.name == d.name)) {
                node_list[l.source.name] = 1;
                node_list[l.target.name] = 1;
                return 0.8;
            } else {
                return 0.3;
            }
        });     

       local_quqn.labels.style("fill", function(l) {
            if(node_list[l.name] != undefined) {
                return "#33F0FF";
            } else {
                return "black";
            }
        });

       local_quqn.labels.style("fill-opacity", function(l) {
            if(node_list[l.name] != undefined) {
                return 0.8;
            } else {
                return 0.1;              
            }
        });

        local_quqn.node.style("fill", function(l) {
            if(node_list[l.name] != undefined) {
                return "#33F0FF";
            } else {
                return "white";
            }               
        });
        local_quqn.node.style("fill-opacity", function(l) {
            return 1;            
        });
        local_quqn.node.style("stroke-opacity", function(l) {
            return 0.2;            
        });

        local_quqn.marker.style("fill", function(m) {
            if(node_list[m.name] != undefined) {
                return "#33F0FF";
            }        
        });
        local_quqn.marker.style("fill-opacity", function(m) {
            if(node_list[m.name] == undefined) {
                return 0.3;
            }
        });
       local_quqn.images.style("opacity", function(l) {
           return 1;
       });
    }

    on_hover_out_unlight_neighbors(d) {
        var local_quqn = this;
        local_quqn.link.style("stroke", function(l) {
            return local_quqn.linkColour(l.type);
        });

       local_quqn.labels.style("fill", function(l) {
            return "black";
        });

       local_quqn.node.style("fill-opacity", function(l) {
           if(l.H == "0") {
               return 1;
           } else {
               return 0.2;
           }
       });

       local_quqn.node.style("stroke-opacity", function(l) {
           if(l.H == "0") {
               return 0.2;
           } else {
               return 0.1;
           }
       });

       local_quqn.images.style("opacity", function(l) {
           if(l.H == "0") {
               return 1;
           } else {
               return 0.2;
           }
       });

       local_quqn.labels.style("fill-opacity", function(l) {
            if(l.H == "0") {
                return 0.8;
            } else {
                return 0.2;
            }
            
        });

        local_quqn.node.style("fill", function(l) {
            if(l.D == "1") {
                return "red";
            } else {
                if(local_quqn.search_value) {
                    if(l.decleration.toLowerCase().includes(local_quqn.search_value.toLowerCase())) {
                        return "#4EFC68";
                    } else {
                        return local_quqn.circleColour(parseInt(l.inlinks), parseInt(l.outlinks));
                    }
                } else {
                    return local_quqn.circleColour(parseInt(l.inlinks), parseInt(l.outlinks));
                }
            }
        });      

        local_quqn.marker.style("fill", function(m) {
            return "gray";
        });
        local_quqn.marker.style("fill-opacity", function(m) {
            if(m.H == "0") {
                return 0.8;
            } else {
                return 0.2;
            }
        });
        local_quqn.link.style("stroke-opacity", function(l) {
            local_quqn
            if(l.H == "0") {
                return 0.6;
            } else {
                return 0.1;
            }
        }); 
    }
}




