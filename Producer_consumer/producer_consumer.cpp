#include<iostream>
#include<thread>
#include<queue>
#include<mutex>
#include<condition_variable>
#include<chrono>
#include<vector>
#include<stdexcept>

std::queue<int> buffer; //shared buffer
unsigned int MAX_SIZE =5;//buffer size
std::mutex mtx;//mutex for syncronisation
std::condition_variable cv;//condition variable

void producer(int id)
{
	try{
	int value=0;
	while(1)
	{
		std::unique_lock<std::mutex> lock(mtx);
		cv.wait(lock,[]{return buffer.size()<MAX_SIZE;});//wait if buffer is full
		buffer.push(value);
		std::cout<<"Producer "<<id<<" produced "<<value<<std::endl;
		value++;

		lock.unlock();
		cv.notify_all();//Notify consumers
                std::this_thread::sleep_for(std::chrono::milliseconds(100));//simulate work
	}
	}catch(const std::exception&ex)
	{
		std::cout<<"Producer "<<id<<"encountered an error "<<ex.what()<<std::endl;
	}

}
void consumer(int id)
{
	try{
	while(1)
	{
		std::unique_lock<std::mutex> lock(mtx);
		cv.wait(lock,[]{return !buffer.empty();});
		int value =buffer.front();
		buffer.pop();
                std::cout<<"consumer "<<id<<" comsumed "<<value<<std::endl;
		lock.unlock();
		cv.notify_all();//notify all producers
std::this_thread::sleep_for(std::chrono::milliseconds(150));//simulate work

	}
	}catch(const std::exception&ex)
	{
      std::cout<<"consumer "<<id<<" encountered error "<<ex.what()<<std::endl;
	}
}

int main(int argc,char*argv[])
{
	try{
		if(argc!=4)
		{
			throw std::invalid_argument("Usage: ./producer_consumer <buffer_size> <num_producers> <num_consumers>");
        }
		MAX_SIZE=std::stoi(argv[1]);
       int num_producers =std::stoi(argv[2]);
	   int num_consumers =std::stoi(argv[3]);
	    if (MAX_SIZE <= 0 || num_producers <= 0 || num_consumers <= 0) {
            throw std::invalid_argument("All parameters must be positive integers.");
        }
		//create threads
		std::vector<std::thread> producers;
		for(int i=0;i<num_producers;i++)
		{
			producers.emplace_back(producer,i+1);
		}
		std::vector<std::thread> consumers;
		for(int i=0;i<num_consumers;i++)
		{
			consumers.emplace_back(producer,i+1);
		}
	for(auto& t:producers) t.join();
	for(auto& t:consumers) t.join();
	}
	catch(const std::exception&ex){
      std::cout<<"Error in main "<<ex.what()<<std::endl;
	  return EXIT_FAILURE;
	}
	return 0;
}
