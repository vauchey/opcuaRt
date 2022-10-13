import QtQuick 2.5
import QtQuick.Controls 2.0
import QtQuick.Controls.Styles 1.0
import QtQuick.Extras 1.0


//import QtQuick.Controls.Styles 1.4
//import QtQuick.Extras 1.0
  
//import QtLocation 5.3
//import QtLocation 5.6
//import QtPositioning 5.3
import QtLocation 5.9
import QtPositioning 5.6
import QtQuick.Window 2.0
import QtRTMaps 1.0
import QtRTMaps.Widgets 1.0
import QtMultimedia 5.5
import QtQml.Models 2.1
import QtQuick.Layouts 1.2




Image 
{
	// RTMaps QML Viewer Inputs
	//definition des properties
	
	//definition des proprietes d ihm
	property double windowsRatio:0.8 //taille de la fenetre
	property int boxSpacing: 3//7
	property int angleCurves:10//courbure des rectancles
	property int borderWidht:0 //1 //0

	property double ratioHeader: 0.10//ratio de la partie haute

	property double ratioLeftPart: 0.20//ratio de la partie de gauche
	property double ratioRightPart:0.20 //ratio de la partie droite
	property double ratioMapVertical:0.80 //ratio de la partie droite

	//definition des outputs
	property var butOutModeStop:0
	property var butOutshutdown:0

	property var butOutstopbuttonConfirm:0
	property var butOutstopbuttonCancel:0
	property var butOutshutdownbuttonConfirm:0
	property var butOutshutdownbuttonCancel:0
									
	//definition des input gps
	property var latlongAltYaw: [49.2,2.1,0.0,0.0]
	property var latlongAltYaw1: [49.2,2.1,0.0,0.0]
	property var latlongAltYaw2: [49.2,2.1,0.0,0.0]
	property var vehiculeSpeed:-1.0
	property double last_latitude:0
	property double last_longitude:0
	property double last_latitude1:0
	property double last_longitude1:0
	property double last_latitude2:0
	property double last_longitude2:0
	// Variable interne
	property ListModel someModel : ListModel {}
	property ListModel someModel1 : ListModel {}
	property ListModel someModel2 : ListModel {}
	
	//definition des status a afficher
	property var ledNames :[
						"CAM 1 Stream frequency",
						"CAM 2 Stream frequency",
						"GPS Stream frequency",
						"GPS accuracy",
						"Cloud Connection",
						"Batery Measurement Voltage"
						]
						
	property var ledNamesUnitry :[
						"Hz",
						"Hz",
						"Hz",
						"m",
						"Hz",
						"Hz"						
						]
	property var leds: [-1,-1,-1,-1,-1,-1]
	property var ledsWarningExpected: [20.0,20.0,8.0,2.0 ,5.0,-1.0] //valeur en dessus du quel on passe en warning (une valeur negative pour ne pas se soucier des warinings)
	property var ledsErrorExpected:   [1.0 ,1.0 ,1.0,20.0,1.0,1.0] //valeur en dessus du quel on passe en error
	property var ledsMultiplieur:     [1.0 ,1.0 ,1.0,-1.0,1.0,1.0]// permet d'inverser les verifications et de changer la logique (au lieu de verifier en dessous de, on verifie au dessus de
	
	property var batteryValue:-1
	property var batteryMaxValue:14.0
	property var batteryMinValue:11.0
	property var batteryValueNamesUnitry :"V"
	property var battery4CentValue:100.0*((batteryValue-batteryMinValue)/(batteryMaxValue-batteryMinValue))
	
	//check system ready
	property var systemReady:{
							if (
									(leds[0]> ledsErrorExpected[0] )
									&&
									(leds[1]> ledsErrorExpected[1] )
									&&
									(leds[2]> ledsErrorExpected[2] )
									&&
									(leds[3]< ledsErrorExpected[3] )//sufficient accuracy
									&&
									(leds[4]> ledsErrorExpected[4] ) //
									&&
									(leds[5]> ledsErrorExpected[4] )
								)
								{
									1
								}
								else
								{
									0
								}
	}
	
	//definition des gradients 
	property string colorBottomLeft :"#e0e0f8"
	property string colorBottomRight :"#e0e0f8"
	property string colorBottom :"#e0e0f8"
	property string colorRightBox :"#b3e3f7"
	property string colorTopLeft :"#e0e0f8"
	property string colorCenter :"#e0e0f8"
	property string colorTopRight :"#e0e0f8"
	property string colorModeStandBy :"#b3e3f7"
	property string colorStatusNotOk :"#f79f81"
	property string colorStatusOk :"#bef781"
	property string colorOrange:"#fea347" 
	property string colorModeAuto :"#f3f781"
	property string colorModeSupervisory :"#bef781"


	property int animationTime : 200 //1000
	property int animationVisibleTime :500
	property int buttonAnimationTime : 0 //1000
	
	property Gradient gradientGrisClair: Gradient {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: "#e0e0f8" }
	}
	property Gradient gradientButton: Gradient
	{
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: colorBottom }//"#e0e0f8"
	}
	
	property Gradient gradientGreen: Gradient {
    GradientStop { position: 1.0; color: "#ffffff" }
    GradientStop { position: 0.0; color: colorStatusOk }
	}
	property Gradient gradientRed: Gradient {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: colorStatusNotOk }
	}
	property Gradient gradientBlue: Gradient {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: colorModeStandBy }
	}
	property Gradient gradientBlueAuto: Gradient 
	 {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: "#318CE7" }
	}
			  
	property Gradient gradientYellow: Gradient {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: colorModeAuto }
	}

	property Gradient gradientGris: Gradient {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: "#89725b" }
	}

	property Gradient gradientOrange: Gradient {
		GradientStop { position: 1.0; color: "#ffffff" }
		GradientStop { position: 0.0; color: colorOrange }
	}
	
	property int ledTextSize : 10
	property int textFontSize: 20//27
	
	
	MAPSVideoPlayer{
        id: mapsvideoCam1Main
        source: "videoCam1Main"
    }
	
	MAPSVideoPlayer{
        id: mapsvideoCam2Main
        source: "videoCam2Main"
    }

	MAPSVideoPlayer{
        id: mapsvideoCam1
        source: "videoCam1"
    }
	
	MAPSVideoPlayer{
        id: mapsvideoCam2
        source: "videoCam2"
    }

	id: main
	height: Screen.height*windowsRatio
    clip: false
    width: Screen.width*windowsRatio
	Image{
		id:background
		x:parent.x
		y:parent.y
		height:parent.height
		width: parent.width
		source:"./images/background3.JPG"
		anchors.fill:parent
		fillMode: Image.PreserveAspectCrop
	}
	Item{
		id:colorBack
		x:parent.x
		y:parent.y
		height:parent.height
		width: parent.width
		Rectangle{
			height:parent.height
			width: parent.width
			color:"white"
			}
		opacity:0.5
		}
		
	Grid
    {
        id : main_Grid
        rows: 2
        columns: 1
        //anchors.fill: parent
        width: parent.width
        height:parent.height
        spacing: boxSpacing
        //////////////////GRILL DU HAUT
		Item
        {
            id: topgrid
            //width: parent.width*(ratioLeftPart)-(parent.rows*parent.spacing)
            //height: parent.height*ratioHightPart-(parent.columns*parent.spacing)
			z:2
            width: parent.width-parent.spacing
            height:(parent.height*ratioHeader)-parent.spacing
			
			Rectangle
            {
                radius: angleCurves
                //color: colorTopLeft
                gradient: Gradient
                {
                    GradientStop { position: 1.0; color: "#ffffff" }
                    GradientStop { position: 0.0; color: colorTopLeft }//"#e0e0f8"
                }
                border.width: borderWidht
                id: itemLogos
                //width: parent.width
                //height: parent.height

                anchors.rightMargin: boxSpacing
                anchors.leftMargin: boxSpacing
                anchors.bottomMargin: boxSpacing
                anchors.topMargin: boxSpacing
                anchors.fill: parent
				Grid
                {
                    id: topgridLogos
                    width: parent.width
                    height: parent.height
                    rows: 1
                    columns: 4
					
					//status general
					
					
					//logo metropole
					Item
					{
						
						width: (parent.width/parent.columns)
						height: (parent.height/parent.rows)-(boxSpacing*parent.rows)
						Image {
							
							anchors.fill: parent
							fillMode: Image.PreserveAspectFit
							source: "./images/metropole.jpg"
						   }
					}
					
					//logo esigelec
					Item
					{
						id:itemlogoEsigelec
						width: (parent.width/parent.columns)
						height: (parent.height/parent.rows)-(boxSpacing*parent.rows)
						Image {
							//id: imagelogoEsigelec
							anchors.fill: parent
							fillMode: Image.PreserveAspectFit
							source: "./images/logo_ESIGELEC.png"
						   }
					}
					
					//logo lineact
					Item
					{
						id:itemlogoLineact
						width: (parent.width/parent.columns)
						height: (parent.height/parent.rows)-(boxSpacing*parent.rows)
						Image {
							//id: imagelogoEsigelec
							anchors.fill: parent
							fillMode: Image.PreserveAspectFit
							source: "./images/lineact.png"
						   }
					}
					
					//logo litis
					Item
					{
						id:itemlogoLitis
						width: (parent.width/parent.columns)
						height: (parent.height/parent.rows)-(boxSpacing*parent.rows)
						Image {
							//id: imagelogoEsigelec
							anchors.fill: parent
							fillMode: Image.PreserveAspectFit
							source: "./images/logolitis.png"
						   }
					}
					
					
					
				}
			}
		}
		////////////GRILLE du cente verticalement
		
		Item
        {
			z:1
            width: parent.width -parent.spacing
            height:(parent.height*(1.0-ratioHeader)) -parent.spacing //(parent.height*80)/100

			
						
            Grid
            {
                id: gridTop
                //anchors.fill:parent
                width: parent.width
                height:parent.height
                rows: 1
                columns: 3
				
				///////////////GRILLE DE GAUCHE
                Item
                {
                    width: parent.width*ratioLeftPart //(parent.width*15)/100
                    height: parent.height
					
					Rectangle
					{
						anchors.rightMargin: boxSpacing
						anchors.leftMargin: boxSpacing
						anchors.bottomMargin: boxSpacing
						anchors.topMargin: boxSpacing
						anchors.fill: parent
						gradient: gradientGrisClair
						radius: angleCurves
						border.width: borderWidht
						
					}
				}
				
				///////////////GRILLE DU CENTRE
				Item
                {
                    width: parent.width*(1.0-ratioLeftPart-ratioRightPart) //(parent.width*15)/100
                    height: parent.height
					
					Rectangle
					{
						anchors.rightMargin: boxSpacing
						anchors.leftMargin: boxSpacing
						anchors.bottomMargin: boxSpacing
						anchors.topMargin: boxSpacing
						anchors.fill: parent
						gradient: gradientGrisClair
						radius: angleCurves
						border.width: borderWidht
						Grid
						{
							id: gridCentraleHoriz
							//anchors.fill:parent
							width: parent.width
							height:parent.height
							rows: 2
							columns: 1
							Item
							{
								width: parent.width //(parent.width*15)/100
								height: parent.height*ratioMapVertical
							
								Rectangle
								{
									anchors.rightMargin: boxSpacing
									anchors.leftMargin: boxSpacing
									anchors.bottomMargin: boxSpacing
									anchors.topMargin: boxSpacing
									anchors.fill: parent
									gradient: gradientGrisClair
									radius: angleCurves
									border.width: borderWidht
								
									Plugin {
										id: mapProvider
										name : "osm"
										//PluginParameter { name: "osm.mapping.host"; value: "http://localhost/tiles/1.0.0/map/" }
										//PluginParameter { name: "osm.mapping.host"; value: "http://a.tile.thunderforest.com/landscape/" }
										PluginParameter { name: "osm.mapping.host"; value: "http://b.tile.openstreetmap.org/" }
										//name : "here"
										//PluginParameter { name: "here.app_id"; value: "your_app_id" }
										//PluginParameter { name: "here.token"; value: "your_app_code" }
									}
											
											
									/////////////////video centrale
									
								
									////////////////// carte centralle
									Map 
									{
										
										function getCustomMapType()
										{
											for (var i=0; i<map.supportedMapTypes.length; i++)
											{
												if (map.supportedMapTypes[i].style === MapType.CustomMap)
													return map.supportedMapTypes[i]
											}
										}
										
										visible:true
										id: map
										plugin: mapProvider
										activeMapType: getCustomMapType()
										
										anchors.fill: parent
										zoomLevel: maximumZoomLevel-1

										property bool followMe: true
										gesture.onPanStarted: followMe=false
										gesture.onPinchStarted: followMe=false
										gesture.onFlickStarted: followMe=false

										center: QtPositioning.coordinate(latlongAltYaw[0], latlongAltYaw[1])
										onCenterChanged : 
										{//someModel.append({lat:main.latitude, lon:main.longitude});#a la basse 30 poins tous les 10m
											if (someModel.count>100){
												someModel.remove(0,1);
											}
											if (center.distanceTo(QtPositioning.coordinate(last_latitude,last_longitude))>1){
												someModel.append({lat:latlongAltYaw[0], lon:latlongAltYaw[1]});
												last_latitude = latlongAltYaw[0];
												last_longitude = latlongAltYaw[1];
											}
										}
													
										
										// Affichage du marker de position
										MapQuickItem 
										{

											objectName: "marker"
											coordinate { latitude: latlongAltYaw[0]; longitude : latlongAltYaw[1] }
											anchorPoint.x: 12
											anchorPoint.y: 15
											rotation: latlongAltYaw[3]*180.0/3.14156
											sourceItem: Image
														{
															width: 24
															height: 34
															source: "./images/markeur_ami1.PNG"
														}
										}
										
										Repeater
										{
											model: someModel
											MapItemGroup 
											{
												//id: delegateGroup
												MapCircle 
												{
													//id: innerCircle
													color: "red"
													center: QtPositioning.coordinate(model.lat, model.lon)
													radius: 1.0
												}

												Component.onCompleted: map.addMapItemGroup(this)
											}
										}
									
										// Ajout du Bouton zoom +
										Button {
											id: zoom_up
											x: (1/20)*map.width
											y: (1/8)*map.height
											height: (1/8)*map.height
											width: zoom_up.height
											
											enabled: map.zoomLevel<map.maximumZoomLevel
											onClicked: (map.zoomLevel+1>=map.maximumZoomLevel)? map.zoomLevel=map.maximumZoomLevel : map.zoomLevel=map.zoomLevel+1
											text: "+"
										}
										// Ajout du Bouton zoom -
										Button {
											id: zoom_down
											x: (1/20)*map.width
											y: zoom_up.y+zoom_up.height
											height: (1/8)*map.height
											width: zoom_down.height
											
											enabled: map.zoomLevel>map.minimumZoomLevel
											onClicked: (map.zoomLevel-1<=map.minimumZoomLevel)? map.zoomLevel=map.minimumZoomLevel : map.zoomLevel=map.zoomLevel-1
											text: "-"
										}
									}
									
									
									Map 
									{
										
										function getCustomMapType1()
										{
											for (var i=0; i<map1_1.supportedMapTypes.length; i++)
											{
												if (map1_1.supportedMapTypes[i].style === MapType.CustomMap)
													return map1_1.supportedMapTypes[i]
											}
										}
										
										visible:false
										id: map1_1
										plugin: mapProvider
										activeMapType: getCustomMapType1()
										
										anchors.fill: parent
										zoomLevel: maximumZoomLevel-1

										property bool followMe: true
										gesture.onPanStarted: followMe=false
										gesture.onPinchStarted: followMe=false
										gesture.onFlickStarted: followMe=false

										center: QtPositioning.coordinate(latlongAltYaw1[0], latlongAltYaw1[1])
										onCenterChanged : 
										{
											if (someModel1.count>100){
												someModel1.remove(0,1);
											}
											if (center.distanceTo(QtPositioning.coordinate(last_latitude1,last_longitude1))>1){
												someModel1.append({lat:latlongAltYaw1[0], lon:latlongAltYaw1[1]});
												last_latitude1 = latlongAltYaw1[0];
												last_longitude1 = latlongAltYaw1[1];
											}
										}
													
										
										// Affichage du marker de position
										MapQuickItem 
										{

											objectName: "marker"
											coordinate { latitude: latlongAltYaw1[0]; longitude : latlongAltYaw1[1] }
											anchorPoint.x: 12
											anchorPoint.y: 15
											rotation: latlongAltYaw1[3]*180.0/3.14156
											sourceItem: Image
														{
															width: 24
															height: 34
															source: "./images/markeur_ami2.PNG"
														}
										}
										
										Repeater
										{
											model: someModel1
											MapItemGroup 
											{
												//id: delegateGroup
												MapCircle 
												{
													//id: innerCircle
													color: "red"
													center: QtPositioning.coordinate(model.lat, model.lon)
													radius: 1.0
												}

												Component.onCompleted: map.addMapItemGroup(this)
											}
										}
									
										// Ajout du Bouton zoom +
										Button {
											id: zoom_up1
											x: (1/20)*map1_1.width
											y: (1/8)*map1_1.height
											height: (1/8)*map1_1.height
											width: zoom_up1.height
											
											enabled: map1_1.zoomLevel<map1_1.maximumZoomLevel
											onClicked: (map1_1.zoomLevel+1>=map1_1.maximumZoomLevel)? map1_1.zoomLevel=map1_1.maximumZoomLevel : map1_1.zoomLevel=map1_1.zoomLevel+1
											text: "+"
										}
										// Ajout du Bouton zoom -
										Button {
											id: zoom_down1
											x: (1/20)*map1_1.width
											y: zoom_up1.y+zoom_up1.height
											height: (1/8)*map1_1.height
											width: zoom_down1.height
											
											enabled: map1_1.zoomLevel>map1_1.minimumZoomLevel
											onClicked: (map1_1.zoomLevel-1<=map1_1.minimumZoomLevel)? map1_1.zoomLevel=map1_1.minimumZoomLevel : map1_1.zoomLevel=map1_1.zoomLevel-1
											text: "-"
										}
									}
									
									
									Map 
									{
										
										function getCustomMapType2()
										{
											for (var i=0; i<map2_1.supportedMapTypes.length; i++)
											{
												if (map2_1.supportedMapTypes[i].style === MapType.CustomMap)
													return map2_1.supportedMapTypes[i]
											}
										}
										
										visible:false
										id: map2_1
										plugin: mapProvider
										activeMapType: getCustomMapType2()
										
										anchors.fill: parent
										zoomLevel: maximumZoomLevel-1

										property bool followMe: true
										gesture.onPanStarted: followMe=false
										gesture.onPinchStarted: followMe=false
										gesture.onFlickStarted: followMe=false

										center: QtPositioning.coordinate(latlongAltYaw2[0], latlongAltYaw2[1])
										onCenterChanged : 
										{
											if (someModel2.count>100){
												someModel2.remove(0,1);
											}
											if (center.distanceTo(QtPositioning.coordinate(last_latitude2,last_longitude2))>1){
												someModel2.append({lat:latlongAltYaw2[0], lon:latlongAltYaw2[1]});
												last_latitude2 = latlongAltYaw2[0];
												last_longitude2 = latlongAltYaw2[1];
											}
										}
													
										
										// Affichage du marker de position
										MapQuickItem 
										{

											objectName: "marker"
											coordinate { latitude: latlongAltYaw2[0]; longitude : latlongAltYaw2[1] }
											anchorPoint.x: 12
											anchorPoint.y: 15
											rotation: latlongAltYaw2[3]*180.0/3.14156
											sourceItem: Image
														{
															width: 24
															height: 34
															source: "./images/markeur_ami3.PNG"
														}
										}
										
										Repeater
										{
											model: someModel2
											MapItemGroup 
											{
												//id: delegateGroup
												MapCircle 
												{
													//id: innerCircle
													color: "red"
													center: QtPositioning.coordinate(model.lat, model.lon)
													radius: 1.0
												}

												Component.onCompleted: map2_1.addMapItemGroup(this)
											}
										}
									
										// Ajout du Bouton zoom +
										Button {
											id: zoom_up2
											x: (1/20)*map2_1.width
											y: (1/8)*map2_1.height
											height: (1/8)*map2_1.height
											width: zoom_up2.height
											
											enabled: map2_1.zoomLevel<map2_1.maximumZoomLevel
											onClicked: (map2_1.zoomLevel+1>=map2_1.maximumZoomLevel)? map2_1.zoomLevel=map2_1.maximumZoomLevel : map2_1.zoomLevel=map2_1.zoomLevel+1
											text: "+"
										}
										// Ajout du Bouton zoom -
										Button {
											id: zoom_down2
											x: (1/20)*map2_1.width
											y: zoom_up2.y+zoom_up2.height
											height: (1/8)*map2_1.height
											width: zoom_down2.height
											
											enabled: map2_1.zoomLevel>map2_1.minimumZoomLevel
											onClicked: (map2_1.zoomLevel-1<=map2_1.minimumZoomLevel)? map2_1.zoomLevel=map2_1.minimumZoomLevel : map2_1.zoomLevel=map2_1.zoomLevel-1
											text: "-"
										}
									}
								}
							}
							Item
							{
								width: parent.width //(parent.width*15)/100
								height: parent.height*(1-ratioMapVertical)
							
								Rectangle
								{
									anchors.rightMargin: boxSpacing
									anchors.leftMargin: boxSpacing
									anchors.bottomMargin: boxSpacing
									anchors.topMargin: boxSpacing
									anchors.fill: parent
									gradient: gradientGrisClair
									radius: angleCurves
									border.width: borderWidht
									Grid
									{
										width:parent.width
										height:parent.height //*(1-gaugeRatio) //(parent.height*40)/100
										spacing: boxSpacing
										rows: 1//3
										columns: 1//5
										Item
										{
											width: (parent.width/parent.columns)-(parent.spacing)
											height: (parent.height/parent.rows)-(parent.spacing)
											Rectangle
											{
												anchors.rightMargin: boxSpacing
												anchors.leftMargin: boxSpacing
												anchors.bottomMargin: boxSpacing
												anchors.topMargin: boxSpacing
												anchors.fill: parent
												gradient: gradientGrisClair
												radius: angleCurves
												border.width: borderWidht
									
												
												//zone du bas
											}
											
										}
									}
								}
							}
						}
					}
				}
				
				/////////////GRILLE DE DROITE
				Item
                {
                    width: parent.width*(ratioRightPart) //(parent.width*15)/100
                    height: parent.height
					Grid
					{
						id: gridRight
						//anchors.fill:parent
						width: parent.width
						height:parent.height
						rows: 3
						columns: 1
						Item
						{
							width: parent.width //(parent.width*15)/100
							height: parent.height/parent.rows
						
							Rectangle
							{
								anchors.rightMargin: boxSpacing
								anchors.leftMargin: boxSpacing
								anchors.bottomMargin: boxSpacing
								anchors.topMargin: boxSpacing
								anchors.fill: parent
								gradient: gradientBlue
								radius: angleCurves
								border.width: borderWidht
								id:video1Rectangle
								
								MouseArea
								{
									id: videocursor1
									anchors.fill: parent
									hoverEnabled: true
									onClicked: showVideo(0)
								}
								Item
								{
									x:boxSpacing*2
									y:boxSpacing*2
									width: parent.width-boxSpacing*4
									height: parent.height-boxSpacing*4
									Rectangle
									{
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										gradient: gradientBlue
										radius: angleCurves
										Map 
										{
											x:boxSpacing
											y:boxSpacing
											width: parent.width-boxSpacing*2
											height: parent.height-boxSpacing*2
											
											function getCustomMapType()
											{
												for (var i=0; i<map.supportedMapTypes.length; i++)
												{
													if (map.supportedMapTypes[i].style === MapType.CustomMap)
														return map.supportedMapTypes[i]
												}
											}
										
											id: map2_2
											plugin: mapProvider
											activeMapType: getCustomMapType()
											
											anchors.fill: parent
											zoomLevel: maximumZoomLevel-1

											property bool followMe: true
											gesture.onPanStarted: followMe=false
											gesture.onPinchStarted: followMe=false
											gesture.onFlickStarted: followMe=false
											

											center: QtPositioning.coordinate(latlongAltYaw2[0], latlongAltYaw2[1])
											onCenterChanged : 
											{//someModel.append({lat:main.latitude, lon:main.longitude});#a la basse 30 poins tous les 10m
												if (someModel.count>100){
													someModel.remove(0,1);
												}
												if (center.distanceTo(QtPositioning.coordinate(last_latitude,last_longitude))>1){
													someModel.append({lat:latlongAltYaw2[0], lon:latlongAltYaw2[1]});
													last_latitude = latlongAltYaw2[0];
													last_longitude = latlongAltYaw2[1];
												}
											}
														
											
											// Affichage du marker de position
											MapQuickItem 
											{

												objectName: "marker"
												coordinate { latitude: latlongAltYaw2[0]; longitude : latlongAltYaw2[1] }
												anchorPoint.x: 12
												anchorPoint.y: 15
												rotation: latlongAltYaw2[3]*180.0/3.14156
												sourceItem: Image
															{
																width: 24
																height: 34
																source: "./images/markeur_ami3.PNG"
															}
											}
											
											Repeater
											{
												model: someModel
												MapItemGroup 
												{
													id: delegateGroup2_2
													MapCircle 
													{
														//id: innerCircle
														color: "red"
														center: QtPositioning.coordinate(model.lat, model.lon)
														radius: 1.0
													}

													Component.onCompleted: map2_2.addMapItemGroup(this)
												}
											}
											MouseArea
											{
													//id: videocursorX
													anchors.fill: parent
													hoverEnabled: true
													onClicked: showVideo(0)
											}
											
										}
									}
								}
									
							}
						}
						Item
						{
							width: parent.width //(parent.width*15)/100
							height: parent.height/parent.rows
						
							Rectangle
							{
								anchors.rightMargin: boxSpacing
								anchors.leftMargin: boxSpacing
								anchors.bottomMargin: boxSpacing
								anchors.topMargin: boxSpacing
								anchors.fill: parent
								gradient: gradientBlue
								radius: angleCurves
								border.width: borderWidht
								id:video2Rectangle
								
								
								MouseArea
								{
									id: videocursor2
									anchors.fill: parent
									hoverEnabled: true
									onClicked: showVideo(1)
								}
								
								Item
								{
									x:boxSpacing*2
									y:boxSpacing*2
									width: parent.width-boxSpacing*4
									height: parent.height-boxSpacing*4
									Rectangle
									{
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										gradient: gradientBlue
										radius: angleCurves
										Map 
										{
											x:boxSpacing
											y:boxSpacing
											width: parent.width-boxSpacing*2
											height: parent.height-boxSpacing*2
											
											function getCustomMapType()
											{
												for (var i=0; i<map.supportedMapTypes.length; i++)
												{
													if (map.supportedMapTypes[i].style === MapType.CustomMap)
														return map.supportedMapTypes[i]
												}
											}
										
											id: map1_2
											plugin: mapProvider
											activeMapType: getCustomMapType()
											
											anchors.fill: parent
											zoomLevel: maximumZoomLevel-1

											property bool followMe: true
											gesture.onPanStarted: followMe=false
											gesture.onPinchStarted: followMe=false
											gesture.onFlickStarted: followMe=false
											

											center: QtPositioning.coordinate(latlongAltYaw1[0], latlongAltYaw1[1])
											onCenterChanged : 
											{//someModel.append({lat:main.latitude, lon:main.longitude});#a la basse 30 poins tous les 10m
												if (someModel.count>100){
													someModel.remove(0,1);
												}
												if (center.distanceTo(QtPositioning.coordinate(last_latitude,last_longitude))>1){
													someModel.append({lat:latlongAltYaw1[0], lon:latlongAltYaw1[1]});
													last_latitude = latlongAltYaw1[0];
													last_longitude = latlongAltYaw1[1];
												}
											}
														
											
											// Affichage du marker de position
											MapQuickItem 
											{

												objectName: "marker"
												coordinate { latitude: latlongAltYaw1[0]; longitude : latlongAltYaw1[1] }
												anchorPoint.x: 12
												anchorPoint.y: 15
												rotation: latlongAltYaw1[3]*180.0/3.14156
												sourceItem: Image
															{
																width: 24
																height: 34
																source: "./images/markeur_ami2.PNG"
															}
											}
											
											Repeater
											{
												model: someModel
												MapItemGroup 
												{
													id: delegateGroup1_2
													MapCircle 
													{
														//id: innerCircle
														color: "red"
														center: QtPositioning.coordinate(model.lat, model.lon)
														radius: 1.0
													}

													Component.onCompleted: map1_2.addMapItemGroup(this)
												}
											}
										
											MouseArea{
												//id: videocursorX
												anchors.fill: parent
												hoverEnabled: true
												onClicked: showVideo(1)
											}
										}
									}
								}
							}
						}
						Item
						{
							width: parent.width //(parent.width*15)/100
							height: parent.height/parent.rows
						
							Rectangle
							{
								anchors.rightMargin: boxSpacing
								anchors.leftMargin: boxSpacing
								anchors.bottomMargin: boxSpacing
								anchors.topMargin: boxSpacing
								anchors.fill: parent
								gradient: gradientBlue
								radius: angleCurves
								border.width: borderWidht
								id:video3Rectangle
								
								
								MouseArea{
									//id: videocursor3
									anchors.fill: parent
									hoverEnabled: true
									onClicked: showVideo(2)
								}
								Item
								{
									x:boxSpacing*2
									y:boxSpacing*2
									width: parent.width-boxSpacing*4
									height: parent.height-boxSpacing*4
									Rectangle
									{
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										gradient: gradientBlue
										radius: angleCurves
										Map 
										{
											x:boxSpacing
											y:boxSpacing
											width: parent.width-boxSpacing*2
											height: parent.height-boxSpacing*2
											
											function getCustomMapType()
											{
												for (var i=0; i<map.supportedMapTypes.length; i++)
												{
													if (map.supportedMapTypes[i].style === MapType.CustomMap)
														return map.supportedMapTypes[i]
												}
											}
										
											id: map2
											plugin: mapProvider
											activeMapType: getCustomMapType()
											
											anchors.fill: parent
											zoomLevel: maximumZoomLevel-1

											property bool followMe: true
											gesture.onPanStarted: followMe=false
											gesture.onPinchStarted: followMe=false
											gesture.onFlickStarted: followMe=false
											

											center: QtPositioning.coordinate(latlongAltYaw[0], latlongAltYaw[1])
											onCenterChanged : 
											{//someModel.append({lat:main.latitude, lon:main.longitude});#a la basse 30 poins tous les 10m
												if (someModel.count>100){
													someModel.remove(0,1);
												}
												if (center.distanceTo(QtPositioning.coordinate(last_latitude,last_longitude))>1){
													someModel.append({lat:latlongAltYaw[0], lon:latlongAltYaw[1]});
													last_latitude = latlongAltYaw[0];
													last_longitude = latlongAltYaw[1];
												}
											}
														
											
											// Affichage du marker de position
											MapQuickItem 
											{

												objectName: "marker"
												coordinate { latitude: latlongAltYaw[0]; longitude : latlongAltYaw[1] }
												anchorPoint.x: 12
												anchorPoint.y: 15
												rotation: latlongAltYaw[3]*180.0/3.14156
												sourceItem: Image
															{
																width: 24
																height: 34
																source: "./images/markeur_ami1.PNG"
															}
											}
											
											Repeater
											{
												model: someModel
												MapItemGroup 
												{
													id: delegateGroup2
													MapCircle 
													{
														//id: innerCircle
														color: "red"
														//{
														//			if( systemReady ==1)
														//			{
														//				"green"
														//			}
														//			else
														//			{
														//				"red"
														//			}
														//		}
														center: QtPositioning.coordinate(model.lat, model.lon)
														radius: 1.0
													}

													Component.onCompleted: map2.addMapItemGroup(this)
												}
											}
										
										
											MouseArea{
												//id: videocursorX
												anchors.fill: parent
												hoverEnabled: true
												onClicked: showVideo(2)
											}
										}
									}
								}
							}
						}
					}
				}
			}
			
			/////////////confirm close popup
			Rectangle
			{
				id:confirmClose
				anchors.rightMargin: boxSpacing
				anchors.leftMargin: boxSpacing
				anchors.bottomMargin: boxSpacing
				anchors.topMargin: boxSpacing
				//anchors.fill: parent
				
				width : parent.width/2.0
                height: parent.height/4.0
				x:(parent.width/2.0)-width/2.0
				y:(parent.height/2.0)-height/2.0
				gradient: gradientGrisClair
				radius: angleCurves
				border.width: borderWidht
				visible:false

				Grid
				{
					//anchors.fill:parent
					width : parent.width
					height: parent.height
					rows: 2
					columns: 1
					Item
					{
						x:boxSpacing
						y:boxSpacing
						width: parent.width-boxSpacing*2
						height: 0.5*(parent.height)-boxSpacing*2
						Label
							{
								fontSizeMode:Text.Fit
								width:parent.width
								height:parent.height
								text: "Are you to want to close?"
								
								anchors.rightMargin: boxSpacing
								anchors.leftMargin: boxSpacing
								wrapMode: Text.WordWrap
								font.bold: true
								//anchors.fill: parent
								//font.pixelSize: textFontSize
								font.pixelSize:ledTextSize*2
								horizontalAlignment: Text.AlignHCenter
								verticalAlignment: Text.AlignVCenter
								
							}
					}
					Item
					{
						x:boxSpacing
						y:boxSpacing
						width: parent.width-boxSpacing*2
						height: 0.5*parent.height-boxSpacing*2
						Rectangle
						{
							
							radius: angleCurves
							anchors.rightMargin: boxSpacing
							anchors.leftMargin: boxSpacing
							anchors.bottomMargin: boxSpacing
							anchors.topMargin: boxSpacing
							anchors.fill: parent
							border.width: borderWidht
							gradient: gradientGrisClair
							Grid
							{
								//anchors.fill:parent
								width : parent.width
								height: parent.height
								rows: 1
								columns: 2
								Item
								{
									x:boxSpacing
									y:boxSpacing
									width: parent.width/parent.columns - boxSpacing*2
									height: parent.height - boxSpacing*2
									Rectangle
									{
										id: stopbuttonConfirm//but3Rectangle
										radius: angleCurves
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										border.width: borderWidht
										gradient: gradientRed
										
										states: [
										State {when: (butOutstopbuttonConfirm == 0 );
											name: "On"
											PropertyChanges { target: stopbuttonConfirm; gradient: gradientBlue}
										},
										State {when: (butOutstopbuttonConfirm != 0 );
											name: "Off"
											PropertyChanges { target: stopbuttonConfirm; gradient: gradientGris}
										}
										]

										transitions: [
										Transition {
											from: "*"
											to: "*"
											ColorAnimation { target: stopbuttonConfirm; duration: buttonAnimationTime}
										}
										]

										MouseArea 
										{
											width: parent.width
											height: parent.height
											onExited: {  butOutstopbuttonConfirm =0;confirmClose.visible=false;
											}
											onEntered: {  
												butOutstopbuttonConfirm =1;
											}
										}

										Label
										{
											fontSizeMode:Text.Fit
											text: "Yes"
											wrapMode: Text.WordWrap
											font.bold: true
											anchors.fill: parent
											font.pixelSize: textFontSize
											horizontalAlignment: Text.AlignHCenter
											verticalAlignment: Text.AlignVCenter
										}
									}
								}
								Item
								{
									x:boxSpacing
									y:boxSpacing
									width: parent.width/parent.columns - boxSpacing*2
									height: parent.height - boxSpacing*2
									Rectangle
									{
										id: stopbuttonCancel//but3Rectangle
										radius: angleCurves
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										border.width: borderWidht
										gradient: gradientBlue
										
										states: [
										State {when: (butOutstopbuttonCancel == 0 );
											name: "On"
											PropertyChanges { target: stopbuttonCancel; gradient: gradientBlue}
										},
										State {when: (butOutstopbuttonCancel != 0 );
											name: "Off"
											PropertyChanges { target: stopbuttonCancel; gradient: gradientGris}
										}
										]

										transitions: [
										Transition {
											from: "*"
											to: "*"
											ColorAnimation { target: stopbuttonCancel; duration: buttonAnimationTime}
										}
										]

										MouseArea 
										{
											width: parent.width
											height: parent.height
											onExited: {  butOutstopbuttonCancel =0;confirmClose.visible=false;
											}
											onEntered: {  
												butOutstopbuttonCancel =1;
											}
										}

										Label
										{
											fontSizeMode:Text.Fit
											text: "No"
											wrapMode: Text.WordWrap
											font.bold: true
											anchors.fill: parent
											font.pixelSize: textFontSize
											horizontalAlignment: Text.AlignHCenter
											verticalAlignment: Text.AlignVCenter
										}
									}
								}
							}
						}
					}
				}
			}
			
			
			//confirm shutdown popup
			Rectangle
			{
				id:confirmShutdown
				anchors.rightMargin: boxSpacing
				anchors.leftMargin: boxSpacing
				anchors.bottomMargin: boxSpacing
				anchors.topMargin: boxSpacing
				//anchors.fill: parent
				visible:false
				
				width : parent.width/2.0
                height: parent.height/4.0
				x:(parent.width/2.0)-width/2.0
				y:(parent.height/2.0)-height/2.0
				gradient: gradientGrisClair
				radius: angleCurves
				border.width: borderWidht

				Grid
				{
					//anchors.fill:parent
					width : parent.width
					height: parent.height
					rows: 2
					columns: 1
					Item
					{
						x:boxSpacing
						y:boxSpacing
						width: parent.width-boxSpacing*2
						height: 0.5*(parent.height)-boxSpacing*2
						Label
							{
								fontSizeMode:Text.Fit
								width:parent.width
								height:parent.height
								text: "Are you to want to shutdown?"
								
								anchors.rightMargin: boxSpacing
								anchors.leftMargin: boxSpacing
								wrapMode: Text.WordWrap
								font.bold: true
								//anchors.fill: parent
								//font.pixelSize: textFontSize
								font.pixelSize:ledTextSize*2
								horizontalAlignment: Text.AlignHCenter
								verticalAlignment: Text.AlignVCenter
								
							}
					}
					Item
					{
						x:boxSpacing
						y:boxSpacing
						width: parent.width-boxSpacing*2
						height: 0.5*parent.height-boxSpacing*2
						Rectangle
						{
							
							radius: angleCurves
							anchors.rightMargin: boxSpacing
							anchors.leftMargin: boxSpacing
							anchors.bottomMargin: boxSpacing
							anchors.topMargin: boxSpacing
							anchors.fill: parent
							border.width: borderWidht
							gradient: gradientGrisClair
							Grid
							{
								//anchors.fill:parent
								width : parent.width
								height: parent.height
								rows: 1
								columns: 2
								Item
								{
									x:boxSpacing
									y:boxSpacing
									width: parent.width/parent.columns - boxSpacing*2
									height: parent.height - boxSpacing*2
									Rectangle
									{
										id: shutdownbuttonConfirm//but3Rectangle
										radius: angleCurves
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										border.width: borderWidht
										gradient: gradientRed
										
										states: [
										State {when: (butOutshutdownbuttonConfirm == 0 );
											name: "On"
											PropertyChanges { target: shutdownbuttonConfirm; gradient: gradientBlue}
										},
										State {when: (butOutshutdownbuttonConfirm != 0 );
											name: "Off"
											PropertyChanges { target: shutdownbuttonConfirm; gradient: gradientGris}
										}
										]

										transitions: [
										Transition {
											from: "*"
											to: "*"
											ColorAnimation { target: shutdownbuttonConfirm; duration: buttonAnimationTime}
										}
										]

										MouseArea 
										{
											width: parent.width
											height: parent.height
											onExited: {  butOutshutdownbuttonConfirm =0;confirmShutdown.visible=false;
											}
											onEntered: {  
												butOutshutdownbuttonConfirm =1;
											}
										}

										Label
										{
											fontSizeMode:Text.Fit
											text: "Yes"
											wrapMode: Text.WordWrap
											font.bold: true
											anchors.fill: parent
											font.pixelSize: textFontSize
											horizontalAlignment: Text.AlignHCenter
											verticalAlignment: Text.AlignVCenter
										}
									}
								}
								Item
								{
									x:boxSpacing
									y:boxSpacing
									width: parent.width/parent.columns - boxSpacing*2
									height: parent.height - boxSpacing*2
									Rectangle
									{
										id: shutdownbuttonCancel//but3Rectangle
										radius: angleCurves
										anchors.rightMargin: boxSpacing
										anchors.leftMargin: boxSpacing
										anchors.bottomMargin: boxSpacing
										anchors.topMargin: boxSpacing
										anchors.fill: parent
										border.width: borderWidht
										gradient: gradientBlue
										
										states: [
										State {when: (butOutshutdownbuttonCancel == 0 );
											name: "On"
											PropertyChanges { target: shutdownbuttonCancel; gradient: gradientBlue}
										},
										State {when: (butOutshutdownbuttonCancel != 0 );
											name: "Off"
											PropertyChanges { target: shutdownbuttonCancel; gradient: gradientGris}
										}
										]

										transitions: [
										Transition {
											from: "*"
											to: "*"
											ColorAnimation { target: shutdownbuttonCancel; duration: buttonAnimationTime}
										}
										]

										MouseArea 
										{
											width: parent.width
											height: parent.height
											onExited: {  butOutshutdownbuttonCancel =0;confirmShutdown.visible=false;
											}
											onEntered: {  
												butOutshutdownbuttonCancel =1;
											}
										}

										Label
										{
											fontSizeMode:Text.Fit
											text: "No"
											wrapMode: Text.WordWrap
											font.bold: true
											anchors.fill: parent
											font.pixelSize: textFontSize
											horizontalAlignment: Text.AlignHCenter
											verticalAlignment: Text.AlignVCenter
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	

	function showVideo(videoChannel)
	{
		//videoChannelSelected=videoChannel
		if(videoChannel ==0)
		{
			//mainOutputVideo.source=mapsvideoCam1Main
			map2_1.visible=true
			map1_1.visible=false
			map.visible=false
			//mainOutputVideo.visible=true
			video1Rectangle.gradient= gradientGris
			video2Rectangle.gradient= gradientBlue
			video3Rectangle.gradient= gradientBlue
		}
		else if(videoChannel ==1)
		{
			//mainOutputVideo.source=mapsvideoCam2Main
			map2_1.visible=false
			map1_1.visible=true
			map.visible=false
			//mainOutputVideo.visible=true
			video1Rectangle.gradient= gradientBlue
			video2Rectangle.gradient= gradientGris
			video3Rectangle.gradient= gradientBlue
		}
		else if(videoChannel ==2)
		{
			map2_1.visible=false
			map1_1.visible=false
			map.visible=true
			//mainOutputVideo.visible=false
			video1Rectangle.gradient= gradientBlue
			video2Rectangle.gradient= gradientBlue
			video3Rectangle.gradient= gradientGris
		}
		else 
		{
			video1Rectangle.gradient= gradientBlue
			video2Rectangle.gradient= gradientBlue
			video3Rectangle.gradient= gradientBlue
		}

	}


	Component.onCompleted:
	{
		//map.clearData();
		
		// Control main QML window properties created by RTMaps
		RTMapsQMLWindow.x=Screen.width/2-width/2 ;
		RTMapsQMLWindow.y=Screen.height/2-height/2;
		RTMapsQMLWindow.show();
	}
}
