import torch
import torch.nn as nn

class ZLPRLoss(nn.Module):
    '''
    ZLPR loss function
    
    This is a loss function created in Su et al. 2022 (https://arxiv.org/abs/2208.02955). It is able to model dependencies between
    classes in multi-label classification problems
    '''

    def __init__(self):
        ''''Constructor for ZLPRLoss class'''
        super(ZLPRLoss, self).__init__()

    def forward(self, inputs,targets):
        ''''''
        total_loss = 0

        # Iterate over each sample in mini-batch
        for i in range(inputs.size(dim=0)):
            # Divide inputs scores into those from positive classes and those from negative classes using one-hot encoded targets
            pos_scores = inputs[i][targets[i] == 1]
            neg_scores = inputs[i][targets[i] == 0]

            # If there are positive classes, cacluate positive class loss
            if pos_scores.numel() > 0:
                pos_loss = torch.log(1 + torch.sum(torch.exp(-pos_scores)))
            else:
                pos_loss = 0

            # If there are negative classes, calculate negative class loss
            if neg_scores.numel() > 0:
                neg_loss = torch.log(1 + torch.sum(torch.exp(neg_scores)))
            else:
                neg_loss = 0

            total_loss += pos_loss + neg_loss

        # Calculate average loss for all samples in mini-batch
        batch_loss = total_loss / inputs.size(dim=0)

        return batch_loss
        