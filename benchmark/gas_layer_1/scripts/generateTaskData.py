import json
import random
import string

def generate_random_address():
    # Generate a random Ethereum address
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_random_string(length):
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits
    # Generate a random string using random.choices
    random_string = ''.join(random.choices(characters, k=length))
    return random_string



def generate_data(n):
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    for _ in range(n):
        _modelCID = generate_random_string(20)
        _infoCID = generate_random_string(20)
        maxRounds = 3
        requiredTrainers = 3

        data1.append(_modelCID)
        data2.append(_infoCID)
        data3.append(maxRounds)
        data4.append(requiredTrainers)
    
    return data1,data2,data3,data4

def main():

    a1 = ["BQAuW13R3v0U27kUV7Kc","CE85QgNWwA5T7khTpIz7","zts1YeHxO7K7TbBzO0n2","1stmISsOk3ExvFL8qzXn","TEPoGPz3l0LM31FBv51U","ULTGimSYKEojSKqhXtKv","uKWJWYtHZdUkNinXBWpy","frnIGW4gSIpjtyahYUE6","iH95SJA9YPzKs5NBm4rl","BHepirmRLnbfWz3m52b3","4HsgrcLlvlmYiHjs7D6O","IKlqMCWwnQ9wqkwJqs57","y7ekeTRkyyiR6V6WrMJG","PulRpfpuxDjUa7nN9bIE","Havq1BB6jHa7uVDSDAS6","RLVmcYNQa0NnwpcCz89V","NlUsknOwj7w70AatA2Fa","AnlnR2h54tLj2QOqWLYQ","vo8Ixi6LcwOpRyeyjwu0","WB24wAbQXHxmewbZlz9h","GdkOf05wCHxSrMLFfwJ6","MpRUxYsdn1jhPzGAuX2i","5RbmQG11C2JRKGzgEqhh","ditgL9VQ0m3onadtqW1t","brKQD4EZd7I2QmcRXbKQ","dG1gGBxdSNa68Es4NmiD","s6BhmSbjLrrC0RIVz9o2","Xhbqci3wodN86V438cCy","V3EgZ1QAqlX79lYI764r","aY4pOzdcmm2cjYYOQiHo","hesfxU1tRnq2vA4LyFUV","1q20eFZUNYc1wWnBxSIG","rKbG45UhM7g4indcg7Yj","GLkPUdJoPyecl4nqzLlw","IJ6hGtiNaPYbeyXyowgX","rDzTSfAgKemRRqdERsSG","jcyGFgCGCaEvSa3fk48M","rCR6gJE7gUZjghc0TeHC","DkSuMJRIVVcIYspiwYJ1","Xp1sjXgZT1DMoIZ0YTVc","hqmZdcDs0MAoMGQjQZlN","7Zys8fiQO8Cj1jYThsyx","eL0iFfmZVpdfZzMxH8GH","IGUOfE7i8VygaITDrtSA","kpasdE8e1uprG1Cv58Sy","fYIxjSA2ZmHP7VFSIdT3","XXBARL1RnvvPYg4FXfOL","IxLNdomSKdo7e1xzQvIG","Dp85UQ1G5i2Jqfb22EF9","lPpHWlcS2cJeRc4C3s3a"]
    a2 = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
    a1 = a1[0:25]
    a2 = a2[0:25]
    print(len([["0x17d400c99aea6cbd0dec0d59b260b14bce0c81f3","0x18273cbb09cf997570b0cc490e876fa85318e40f","0x7ca09665bd006d123e9091b445a5ea673db9e299"],["0x50744544c41a3e46b375f58a0707de8ccfe5af1f","0x06c18873ef7b5876478655450187ba9e46e81e17","0xebd34aee59d7b93025b85404d55e46e3891e4dfc"],["0x58ccd56107f1f1564bd4af4ae6c34cebcd111630","0x2a179aef665669beb254b3c7fd149a4c35c29bd5","0x352622f5e783c9917a232b837e92fdd806b35f1f"],["0x6826cfd82fb1fda0129e682c99fe75b0e2c7a909","0xa90aa59aef4d1f29d96c479acc05d7aa72d4f8f9","0x92128e0c2247ebc18b04ad1202f022cb39142fcc"],["0xf2c2a80f95e0b67eba2e6ecf28694c08693b8ec7","0xc9f416446e12adec4d92e708b90be74e606d9470","0x0eef36e6c777ef746e789c6dd5b597bd98c78f14"],["0x97f4343a5ba2eb39cde0b9a061b3ac6652b762d7","0x9b2c2962da4d0ca18e32be81b7aa10e215de39fc","0xf64177fce821d9ed19c96abea45029c789e74c2d"],["0x6cf78f7d00bd73bfc964ea4206e1675c7a8df79a","0x5d39455c47d2d371e837debf41804e261accba39","0x58f315d34bfe52143594971b5b419dc2aa8fda6d"],["0x64ba1ee09e93cc34b29b824cd38f7d0897a4b147","0x9c06c03131f23af3265447e32ca4b10b26732d74","0x4efa86e789b3d47e7e5a956002286e21e52c5e94"],["0xc2e1144208be06ab3c991f4cd9fc6a2ad7f77261","0xab183795d6cd4f07460490e3d73abfc93eb0c121","0xef649a037bfae1539b7296fa7f5762d505c3d2f7"],["0x4803d9283730ac3fc0a7b68f9aa1d3e3ac68d5b3","0x07cd8b17e6cae0339e9783e48b24e5ae298c4c42","0xf42b8de56e0763cb34e44fde778676b1f50a3f03"],["0xd6cf4cccdb438b3f2ca83b87f74313f4026a5a1e","0x896e71a864e1920e69ee6fa703a277f78488a4cc","0x03922d3b2cc42ef69c51767f34089fbeff0a715a"],["0xac2b625c3a0c2ace0004d11b9fed08de4294bc62","0xbac149831808462fa6db40c87fb3d8f3e5810cc8","0x9b5b88b20f24ee69dcbe05843680e7e87e1f173b"],["0x1198b99c3561f4e942a1a687cd03c1a6ff4e714e","0x27b1d4b2119b223dc52d81ec6f117e73995ea435","0x1c2e2821d26b0d22c16fcf56aeb114ce1e1e72ef"],["0x8f63590bd68b013426cbfdf9e06a37873eec7479","0xfb0a437ecb484adc7140e774bf822017c3d5727b","0x1a283cd2183961c87a4858ce37a90a608580bf04"],["0xbf4f1f8b7629a33604299dfdbfa59280ef090111","0xe3cbf094fb85d58ab87fdc0f41e904bfd6b87f36","0x47f7ff744dc4464e629dd323bcbf6ce6985441f2"],["0xe527c79b90be0f81cb515b7dc164e05a63700c45","0xdc66d57b6c4a0bf6012aef01203a2f645eab339e","0xb493644bfacd23c969fc86ec3e66af38d8f9ff03"],["0x01897da8741c8bc6f00df7b0111e6125b0bde69a","0x42a331cac3e2dbd88ba9da4fe3958d90d143a9be","0xccf21bb259b5137638a8a88ccdf58d848999e0ae"],["0x4b6a37d32825cf0be12494eb3d26b882e1be9ad0","0x7f194d695dc413b771f7833d04b74e22ebe8adf2","0xb61a611cec91eaa9408e699d2e8b8400fd1751ec"],["0x17d400c99aea6cbd0dec0d59b260b14bce0c81f3","0x18273cbb09cf997570b0cc490e876fa85318e40f","0x7ca09665bd006d123e9091b445a5ea673db9e299"],["0x50744544c41a3e46b375f58a0707de8ccfe5af1f","0x06c18873ef7b5876478655450187ba9e46e81e17","0xebd34aee59d7b93025b85404d55e46e3891e4dfc"],["0x58ccd56107f1f1564bd4af4ae6c34cebcd111630","0x2a179aef665669beb254b3c7fd149a4c35c29bd5","0x352622f5e783c9917a232b837e92fdd806b35f1f"],["0x6826cfd82fb1fda0129e682c99fe75b0e2c7a909","0xa90aa59aef4d1f29d96c479acc05d7aa72d4f8f9","0x92128e0c2247ebc18b04ad1202f022cb39142fcc"],["0xf2c2a80f95e0b67eba2e6ecf28694c08693b8ec7","0xc9f416446e12adec4d92e708b90be74e606d9470","0x0eef36e6c777ef746e789c6dd5b597bd98c78f14"],["0x97f4343a5ba2eb39cde0b9a061b3ac6652b762d7","0x9b2c2962da4d0ca18e32be81b7aa10e215de39fc","0xf64177fce821d9ed19c96abea45029c789e74c2d"],["0x6cf78f7d00bd73bfc964ea4206e1675c7a8df79a","0x5d39455c47d2d371e837debf41804e261accba39","0x58f315d34bfe52143594971b5b419dc2aa8fda6d"],["0xa5bb8a01b12add856a739a23d529da3e944df56b","0x6c192c53d7b652f58d5a12a42dd5085377bfcc68","0x326ec2f31fd82146531c2f37726aeaceda3f23e1"],["0x0470883ba155c6c6b91c51c60169fe94d88ec902","0xf12208ad7ef22cdf531f45a951fb39b5097d733b","0xf091f0b5d49e38c576f6df7cf35925358eca73d8"],["0x6b8f9d192b1e4e2bf850cc448d2412f38bdfb54f","0xb3b3ee9077a76470261c17886d0e88759e3b631a","0xbea6c70e2b7cee604dad264e41e56c01d34c3964"],["0x79f08206629d4b78e27ed14a00c3840aba0327ba","0x8204b56b6516fd59ce05a8ebc9a1b8285d5f13b0","0x1ec13d5a745d3e3c8be3336e016d704203e59109"],["0x17854d0261c1c4920fd4ef4801de51eeda58fb87","0x97357bcad9dba9b6d292f284bcc930297008b9a7","0x684a233ab9f241f2d26d79f9e4859ab8ff52331b"],["0x39c284847ff057f1637aba4078b1c3b702fe3cd3","0xa3c50266b6938c4dd54e18a7a5c023a291527877","0xd5f9c3eead100b3bc2e39dc7a7a3dd4608bb3cd3"],["0x17d400c99aea6cbd0dec0d59b260b14bce0c81f3","0xbb399ca5a86e934d4147eea51a4a2d100945a2ba","0x0eef36e6c777ef746e789c6dd5b597bd98c78f14"],["0x5d611c96401bc9f81d0703e06ab07fdaea1bedb8","0x9a1cbf4480eb285e37d613a2effc6277bf65965a","0x5172fcfcbd5d230afab221420729a0c88734b905"],["0x81a636b0fe4044b704796e1e269bfe97326857dc","0xb9dcf84e2b38ce5e8a911720e06c3e214ad6973c","0xd2f16f983a316ae4e0bfe2ddeac6c79c9677de4b"],["0xb98a5d190fce0432d3c43446dd1cb203c9cfa33f","0x1bce7efd5013aa7193262399b9f8dc8f65101702","0xf64ae78a7bac6f5ed392ea11d3d4732e87824488"],["0x0f587557d41e610db09e5310d95552f831babcc0","0x20dbc09a29ada4d5a59e25e08b6728b1f04ca2e0","0x8ddab104b9b02791c0edcf0849ec0c658822e542"],["0x4a01575ec95486671e5dca4405c793a854b44a23","0x83f357d8828eb272441be41ded6b215eef6a6436","0x83afb65ae6fd60eea83d7755af3e5b94a59230c0"],["0xa7e6d1dc64bb2ddff6b98955c0f0b0ba974bb150","0x9f41b7a4a944f6fea6847cf71826402255121642","0xbcc542bb57ebdf08f6e486d09ccb5dfbf469da2b"],["0xa1415e6d7283dcf6d319d41524c0aa47ae3b0a3d","0x24d4967ca9e52a90ee2e4b36d851e8913426bf59","0xfde5fe4f45ff725e0dbd83195d1add9c9e8267f0"],["0xc4c11de728107505ce2c57a4cc3d7f2c98852c6f","0xf43100eef70e96f0bbdf91c02e4e45182ac76433","0x964e52be435c597670791e7b93b698e334fe5a39"]]))

    print(len(["hhhh","hhhh","hhhh","hhhh","hhhh","hhhh","hhhh","hhhh","hhhh","hhhh","ggg","ggg","ggg","ggg","ggg","ggg","ggg","ggg","ggg","ggg"]))

    # n = 100  # Number of items to generate
    # data1, data2, data3, data4 = generate_data(n)

    # # Write to JSON file
    # with open('taskData.txt', 'w') as txt_file:
    #     txt_file.write(str(data1) + '\n')
    #     txt_file.write(str(data2) + '\n')
    #     txt_file.write(str(data3) + '\n')
    #     txt_file.write(str(data4) + '\n')
if __name__ == "__main__":
    main()
