import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np # Importation nécessaire pour ce code

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)
        self.move_cmd = Twist()

    def lidar_callback(self, msg):
        # --- NOUVELLE LOGIQUE : VISION EN CÔNE ---
        
        # 1. On récupère toutes les distances
        distances = np.array(msg.ranges)
        
        # 2. On définit un "cône de vision" devant le robot
        # On prend les 30 points du centre (15 à gauche, 15 à droite)
        num_points = len(distances)
        center_index = num_points // 2
        cone_points = distances[center_index-15 : center_index+15]
        
        # 3. On nettoie les données (on enlève les valeurs 'inf' ou 'nan')
        # On ne garde que les vraies distances mesurées
        valid_distances = cone_points[np.isfinite(cone_points)]
        
        # 4. On trouve la distance la plus proche dans ce cône
        if len(valid_distances) > 0:
            dist_min_devant = np.min(valid_distances)
        else:
            # Si le laser ne voit rien du tout, on met une valeur sûre
            dist_min_devant = 10.0

        # --- DÉCISION DE DEMI-TOUR ---
        # Si N'IMPORTE QUOI est dans le cône à moins de 1.1m
        if dist_min_devant < 1.1: 
            self.get_logger().info('OBSTACLE DANS LE CÔNE ! Demi-tour en cours...')
            # ARRÊT IMMÉDIAT de l'avance
            self.move_cmd.linear.x = 0.0 
            # ROTATION TRÈS FORTE pour un demi-tour rapide
            self.move_cmd.angular.z = 2.0 
        else:
            self.get_logger().info('CÔNE LIBRE. J\'avance.')
            # Vitesse de croisière
            self.move_cmd.linear.x = 0.15
            self.move_cmd.angular.z = 0.0
            
        self.publisher.publish(self.move_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        stop_cmd = Twist()
        node.publisher.publish(stop_cmd)
        node.get_logger().info('Arrêt d\'urgence.')
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()