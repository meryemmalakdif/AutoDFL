import os
import logging
import numpy as np
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import random
from datasets import MNIST_truncated, CIFAR10_truncated, CIFAR100_truncated, ImageFolder_custom, SVHN_custom, FashionMNIST_truncated, CustomTensorDataset, CelebA_custom, FEMNIST, Generated, genData
from math import sqrt

import torch.nn as nn

import torch.optim as optim
import torchvision.utils as vutils
import time
import random



logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def mkdirs(dirpath):
    try:
        os.makedirs(dirpath)
    except Exception as _:
        pass

def load_mnist_data(datadir):

    transform = transforms.Compose([transforms.ToTensor()])

    mnist_train_ds = MNIST_truncated(datadir, train=True, download=True, transform=transform)
    mnist_test_ds = MNIST_truncated(datadir, train=False, download=True, transform=transform)

    X_train, y_train = mnist_train_ds.data, mnist_train_ds.target
    X_test, y_test = mnist_test_ds.data, mnist_test_ds.target

    X_train = X_train.data.numpy()
    y_train = y_train.data.numpy()
    X_test = X_test.data.numpy()
    y_test = y_test.data.numpy()

    return (X_train, y_train, X_test, y_test)

def load_fmnist_data(datadir):

    transform = transforms.Compose([transforms.ToTensor()])

    mnist_train_ds = FashionMNIST_truncated(datadir, train=True, download=True, transform=transform)
    mnist_test_ds = FashionMNIST_truncated(datadir, train=False, download=True, transform=transform)

    X_train, y_train = mnist_train_ds.data, mnist_train_ds.target
    X_test, y_test = mnist_test_ds.data, mnist_test_ds.target

    X_train = X_train.data.numpy()
    y_train = y_train.data.numpy()
    X_test = X_test.data.numpy()
    y_test = y_test.data.numpy()

    return (X_train, y_train, X_test, y_test)

def load_svhn_data(datadir):

    transform = transforms.Compose([transforms.ToTensor()])

    svhn_train_ds = SVHN_custom(datadir, train=True, download=True, transform=transform)
    svhn_test_ds = SVHN_custom(datadir, train=False, download=True, transform=transform)

    X_train, y_train = svhn_train_ds.data, svhn_train_ds.target
    X_test, y_test = svhn_test_ds.data, svhn_test_ds.target

    # X_train = X_train.data.numpy()
    # y_train = y_train.data.numpy()
    # X_test = X_test.data.numpy()
    # y_test = y_test.data.numpy()

    return (X_train, y_train, X_test, y_test)


def load_cifar10_data(datadir):

    transform = transforms.Compose([transforms.ToTensor()])

    cifar10_train_ds = CIFAR10_truncated(datadir, train=True, download=True, transform=transform)
    cifar10_test_ds = CIFAR10_truncated(datadir, train=False, download=True, transform=transform)

    X_train, y_train = cifar10_train_ds.data, cifar10_train_ds.target
    X_test, y_test = cifar10_test_ds.data, cifar10_test_ds.target

    # y_train = y_train.numpy()
    # y_test = y_test.numpy()

    return (X_train, y_train, X_test, y_test)

def load_celeba_data(datadir):

    transform = transforms.Compose([transforms.ToTensor()])

    celeba_train_ds = CelebA_custom(datadir, split='train', target_type="attr", download=True, transform=transform)
    celeba_test_ds = CelebA_custom(datadir, split='test', target_type="attr", download=True, transform=transform)

    gender_index = celeba_train_ds.attr_names.index('Male')
    y_train =  celeba_train_ds.attr[:,gender_index:gender_index+1].reshape(-1)
    y_test = celeba_test_ds.attr[:,gender_index:gender_index+1].reshape(-1)

    # y_train = y_train.numpy()
    # y_test = y_test.numpy()

    return (None, y_train, None, y_test)

def load_femnist_data(datadir):
    transform = transforms.Compose([transforms.ToTensor()])

    mnist_train_ds = FEMNIST(datadir, train=True, transform=transform, download=True)
    mnist_test_ds = FEMNIST(datadir, train=False, transform=transform, download=True)

    X_train, y_train, u_train = mnist_train_ds.data, mnist_train_ds.targets, mnist_train_ds.users_index
    X_test, y_test, u_test = mnist_test_ds.data, mnist_test_ds.targets, mnist_test_ds.users_index

    X_train = X_train.data.numpy()
    y_train = y_train.data.numpy()
    u_train = np.array(u_train)
    X_test = X_test.data.numpy()
    y_test = y_test.data.numpy()
    u_test = np.array(u_test)

    return (X_train, y_train, u_train, X_test, y_test, u_test)

def load_cifar100_data(datadir):
    transform = transforms.Compose([transforms.ToTensor()])

    cifar100_train_ds = CIFAR100_truncated(datadir, train=True, download=True, transform=transform)
    cifar100_test_ds = CIFAR100_truncated(datadir, train=False, download=True, transform=transform)

    X_train, y_train = cifar100_train_ds.data, cifar100_train_ds.target
    X_test, y_test = cifar100_test_ds.data, cifar100_test_ds.target

    # y_train = y_train.numpy()
    # y_test = y_test.numpy()

    return (X_train, y_train, X_test, y_test)


def load_tinyimagenet_data(datadir):
    transform = transforms.Compose([transforms.ToTensor()])
    xray_train_ds = ImageFolder_custom(datadir+'./train/', transform=transform)
    xray_test_ds = ImageFolder_custom(datadir+'./val/', transform=transform)

    X_train, y_train = np.array([s[0] for s in xray_train_ds.samples]), np.array([int(s[1]) for s in xray_train_ds.samples])
    X_test, y_test = np.array([s[0] for s in xray_test_ds.samples]), np.array([int(s[1]) for s in xray_test_ds.samples])

    return (X_train, y_train, X_test, y_test)

def record_net_data_stats(y_train, net_dataidx_map, logdir):
    """
    the returned net_cls_counts is an array where each element represents a participating party and is an object of key-value where
        key : a class
        value : number of samples with that class in the party s dataset portion  
    """

    net_cls_counts = {}

    # net_i is the key 
    # net_dataidx_map is the value
    for net_i, dataidx in net_dataidx_map.items():
        # dataidx is the indexes assigned to a participating party net_i
        # so basically here we are extracting all the unique classes found within the assigned partition to a specific party net_i
        # This means that along with the unique elements (unq), you also get the count of each unique element in the array (unq_cnt)
        unq, unq_cnt = np.unique(y_train[dataidx], return_counts=True)
        tmp = {unq[i]: unq_cnt[i] for i in range(len(unq))}
        net_cls_counts[net_i] = tmp

    logger.info('Data statistics: %s' % str(net_cls_counts))

    return net_cls_counts

def partition_data(dataset, datadir, logdir, partition, n_parties, beta=0.4):
    #np.random.seed(2020)
    #torch.manual_seed(2020)
    """
    net_dataidx_map [i: batch_idx[i] which is an array of all the indices of the assigned samples ]
    to access the real dataset portion we need to extract from the mnist original dataset samples corresponding to these indices
    """

    if dataset == 'mnist':
        X_train, y_train, X_test, y_test = load_mnist_data(datadir)
    elif dataset == 'fmnist':
        X_train, y_train, X_test, y_test = load_fmnist_data(datadir)
    elif dataset == 'cifar10':
        X_train, y_train, X_test, y_test = load_cifar10_data(datadir)
    elif dataset == 'svhn':
        X_train, y_train, X_test, y_test = load_svhn_data(datadir)
    elif dataset == 'celeba':
        X_train, y_train, X_test, y_test = load_celeba_data(datadir)
    elif dataset == 'femnist':
        X_train, y_train, u_train, X_test, y_test, u_test = load_femnist_data(datadir)
    elif dataset == 'cifar100':
        X_train, y_train, X_test, y_test = load_cifar100_data(datadir)
    elif dataset == 'tinyimagenet':
        X_train, y_train, X_test, y_test = load_tinyimagenet_data(datadir)
   




    
    n_train = y_train.shape[0]
    n_test = y_test.shape[0]

    if partition == "homo":
        idxs = np.random.permutation(n_train)
        idxs_test = np.random.permutation(n_test)
        batch_idxs = np.array_split(idxs, n_parties)
        batch_idxs_test = np.array_split(idxs_test, n_parties)
        net_dataidx_map = {i: batch_idxs[i] for i in range(n_parties)}
        net_dataidx_map_test = {i: batch_idxs_test[i] for i in range(n_parties)}


    # k represents number of classes

    elif partition == "noniid-labeldir":
        min_size = 0
        min_size_test = 0
        min_require_size = 10
        K = 10
        if dataset == 'cifar100':
            K = 100
        elif dataset == 'tinyimagenet':
            K = 200

        #np.random.seed(2020)
        net_dataidx_map = {}
        net_dataidx_map_test = {}

        while min_size < min_require_size and min_size_test < min_require_size:
            idx_batch = [[] for _ in range(n_parties)]
            idx_batch_test = [[] for _ in range(n_parties)]
            for k in range(K):
                idx_k = np.where(y_train == k)[0]
                idx_k_test = np.where(y_test == k)[0]
                np.random.shuffle(idx_k)
                np.random.shuffle(idx_k_test)
                proportions = np.random.dirichlet(np.repeat(beta, n_parties))
                proportions_test = np.random.dirichlet(np.repeat(beta, n_parties))
                # logger.info("proportions1: ", proportions)
                # logger.info("sum pro1:", np.sum(proportions))
                ## Balance
                proportions = np.array([p * (len(idx_j) < n_train / n_parties) for p, idx_j in zip(proportions, idx_batch)])
                proportions_test = np.array([p * (len(idx_j) < n_test / n_parties) for p, idx_j in zip(proportions, idx_batch_test)])
                # logger.info("proportions2: ", proportions)
                proportions = proportions / proportions.sum()
                proportions_test = proportions_test / proportions_test.sum()
                # logger.info("proportions3: ", proportions)
                proportions = (np.cumsum(proportions) * len(idx_k)).astype(int)[:-1]
                proportions_test = (np.cumsum(proportions_test) * len(idx_k_test)).astype(int)[:-1]
                # logger.info("proportions4: ", proportions)
                idx_batch = [idx_j + idx.tolist() for idx_j, idx in zip(idx_batch, np.split(idx_k, proportions))]
                idx_batch_test = [idx_j + idx.tolist() for idx_j, idx in zip(idx_batch_test, np.split(idx_k_test, proportions_test))]
                
                # I don t like this one mais bon , for now leave it like this
                min_size = min([len(idx_j) for idx_j in idx_batch])
                min_size_test = min([len(idx_j) for idx_j in idx_batch_test])
                # if K == 2 and n_parties <= 10:
                #     if np.min(proportions) < 200:
                #         min_size = 0
                #         break


        for j in range(n_parties):
            np.random.shuffle(idx_batch[j])
            np.random.shuffle(idx_batch_test[j])
            # assign a value to a key within the object
            net_dataidx_map[j] = idx_batch[j]
            net_dataidx_map_test[j] = idx_batch_test[j]

    elif partition == "iid-diff-quantity":
        idxs = np.random.permutation(n_train)
        idxs_test = np.random.permutation(n_test)
        min_size = 0
        while min_size < 10:
            proportions = np.random.dirichlet(np.repeat(beta, n_parties))
            proportions = proportions/proportions.sum()
            min_size = np.min(proportions*len(idxs))
        proportions_test = proportions
        proportions = (np.cumsum(proportions)*len(idxs)).astype(int)[:-1]
        proportions_test = (np.cumsum(proportions_test)*len(idxs_test)).astype(int)[:-1]
        batch_idxs = np.split(idxs,proportions)
        batch_idxs_test = np.split(idxs_test,proportions_test)
        net_dataidx_map = {i: batch_idxs[i] for i in range(n_parties)}
        net_dataidx_map_test = {i: batch_idxs_test[i] for i in range(n_parties)}
        
    elif partition == "mixed":
        min_size = 0
        min_require_size = 10
        K = 10

        net_dataidx_map = {}
        net_dataidx_map_test = {}

        times=[1 for i in range(10)]
        contain=[]
        for i in range(n_parties):
            current=[i%K]
            j=1
            while (j<2):
                ind=random.randint(0,K-1)
                if (ind not in current and times[ind]<2):
                    j=j+1
                    current.append(ind)
                    times[ind]+=1
            contain.append(current)
        net_dataidx_map ={i:np.ndarray(0,dtype=np.int64) for i in range(n_parties)}
        

        min_size = 0
        while min_size < 10:
            proportions = np.random.dirichlet(np.repeat(beta, n_parties))
            proportions = proportions/proportions.sum()
            min_size = np.min(proportions*n_train)

        for i in range(K):
            idx_k = np.where(y_train==i)[0]
            np.random.shuffle(idx_k)

            proportions_k = np.random.dirichlet(np.repeat(beta, 2))
            #proportions_k = np.ndarray(0,dtype=np.float64)
            #for j in range(n_parties):
            #    if i in contain[j]:
            #        proportions_k=np.append(proportions_k ,proportions[j])

            proportions_k = (np.cumsum(proportions_k)*len(idx_k)).astype(int)[:-1]

            split = np.split(idx_k, proportions_k)
            ids=0
            for j in range(n_parties):
                if i in contain[j]:
                    net_dataidx_map[j]=np.append(net_dataidx_map[j],split[ids])
                    ids+=1

   
 
    traindata_cls_counts = record_net_data_stats(y_train, net_dataidx_map, logdir)
    traindata_cls_counts_test = record_net_data_stats(y_test, net_dataidx_map_test, logdir)
    return (X_train, y_train, X_test, y_test, net_dataidx_map, net_dataidx_map_test, traindata_cls_counts, traindata_cls_counts_test)


