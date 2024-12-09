import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque

class DQNNetwork(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dims=[64, 64]):
        """
        Deep Q-Network neural network architecture
        
        Args:
            input_dim (int): Dimension of the input state
            output_dim (int): Number of possible actions
            hidden_dims (list): List of hidden layer dimensions
        """
        super(DQNNetwork, self).__init__()
        
        # Create layers dynamically based on hidden_dims
        layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        """
        Forward pass through the network
        
        Args:
            x (torch.Tensor): Input state
        
        Returns:
            torch.Tensor: Q-values for each action
        """
        return self.network(x)

class DQNAgent:
    def __init__(
        self, 
        input_dim, 
        output_dim, 
        learning_rate=1e-3,
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_end=0.01,
        epsilon_decay=0.995,
        replay_buffer_size=10000,
        batch_size=64,
        target_update_frequency=100
    ):
        """
        Deep Q-Learning Agent
        
        Args:
            input_dim (int): Dimension of the input state
            output_dim (int): Number of possible actions
            learning_rate (float): Learning rate for optimizer
            gamma (float): Discount factor
            epsilon_start (float): Initial exploration rate
            epsilon_end (float): Minimum exploration rate
            epsilon_decay (float): Decay rate for exploration
            replay_buffer_size (int): Size of experience replay buffer
            batch_size (int): Number of experiences to sample per training step
            target_update_frequency (int): Frequency of updating target network
        """
        # Determine device (GPU if available, else CPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Q-Networks
        self.q_network = DQNNetwork(input_dim, output_dim).to(self.device)
        self.target_network = DQNNetwork(input_dim, output_dim).to(self.device)
        
        # Copy weights from q_network to target_network
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Optimizer and loss function
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        
        # Hyperparameters
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update_frequency = target_update_frequency
        
        # Replay buffer
        self.replay_buffer = deque(maxlen=replay_buffer_size)
        
        # Training step counter
        self.steps = 0
    
    def select_action(self, state):
        """
        Select action using epsilon-greedy policy
        
        Args:
            state (np.ndarray): Current environment state
        
        Returns:
            int: Selected action
        """
        # Explore
        if random.random() < self.epsilon:
            return random.randint(0, self.output_dim - 1)
        
        # Exploit
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.q_network(state_tensor)
            return q_values.argmax().item()
    
    def store_transition(self, state, action, reward, next_state, done):
        """
        Store experience in replay buffer
        
        Args:
            state (np.ndarray): Current state
            action (int): Taken action
            reward (float): Received reward
            next_state (np.ndarray): Next state
            done (bool): Episode termination flag
        """
        self.replay_buffer.append((state, action, reward, next_state, done))
    
    def train(self):
        """
        Train the DQN agent using experience replay and target network
        """
        # Check if enough experiences are available
        if len(self.replay_buffer) < self.batch_size:
            return
        
        # Sample batch of experiences
        batch = random.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # Convert to tensors
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        
        # Compute current Q-values
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Compute target Q-values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
        
        # Compute loss
        loss = self.loss_fn(current_q_values, target_q_values)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update target network periodically
        self.steps += 1
        if self.steps % self.target_update_frequency == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
    
    def save_model(self, path):
        """
        Save the model's state dictionary
        
        Args:
            path (str): File path to save model
        """
        torch.save({
            'q_network_state_dict': self.q_network.state_dict(),
            'target_network_state_dict': self.target_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, path)
    
    def load_model(self, path):
        """
        Load a previously saved model
        
        Args:
            path (str): File path to load model from
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
        self.target_network.load_state_dict(checkpoint['target_network_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']

# Example usage (commented out)
# env = gym.make('CartPole-v1')
# agent = DQNAgent(
#     input_dim=env.observation_space.shape[0], 
#     output_dim=env.action_space.n
# )