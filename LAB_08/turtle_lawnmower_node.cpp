#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "turtlesim/Pose.h"
#include "turtlesim/Spawn.h"
#include "turtlesim/Kill.h"

class TurtleLawnmower{
	ros::NodeHandle nh_;
	ros::Subscriber sub_;
	ros::Publisher pub_;
	
	public:
		TurtleLawnmower();
		~TurtleLawnmower();
		void turtleCallback(const turtlesim::Pose::ConstPtr& msg);
};

TurtleLawnmower::TurtleLawnmower(){
	sub_=nh_.subscribe("viktorova_kornjaca/pose", 1, &TurtleLawnmower::turtleCallback, this);
	pub_=nh_.advertise<geometry_msgs::Twist>("viktorova_kornjaca/cmd_vel",1);
}

TurtleLawnmower::~TurtleLawnmower(){
}
void TurtleLawnmower::turtleCallback(const turtlesim::Pose::ConstPtr& msg){
	geometry_msgs::Twist turtle_cmd_vel;

	if (msg->x > 10) {
		turtle_cmd_vel.angular.z=1.57079632679;
	}
	if (msg->x < 1){
		turtle_cmd_vel.angular.z=-1.57079632679;
	}
	turtle_cmd_vel.linear.x=0.45;

	if (msg->y >= 10.5){
		turtle_cmd_vel.linear.x=0;
		turtle_cmd_vel.angular.z=0;
	}
	pub_.publish(turtle_cmd_vel);
}

int main(int argc, char **argv){
	ros::init(argc, argv, "turtle_lawnmower_node");
	ros::NodeHandle node;

	ros::service::waitForService("spawn");

    ros::ServiceClient kill_first_turtle = node.serviceClient<turtlesim::Kill>("kill");
    turtlesim::Kill kill_turtle;
    kill_turtle.request.name = "turtle1";
    kill_first_turtle.call(kill_turtle);

    ros::ServiceClient spawn_left = node.serviceClient<turtlesim::Spawn>("spawn");
    turtlesim::Spawn spawn_turtle;
    spawn_turtle.request.name = "viktorova_kornjaca";
    spawn_turtle.request.x = 1;
    spawn_turtle.request.y = 1;
    spawn_turtle.request.theta = 0;
    spawn_left.call(spawn_turtle);

	TurtleLawnmower TtMower;
	ros::spin();
	return 0;
}

