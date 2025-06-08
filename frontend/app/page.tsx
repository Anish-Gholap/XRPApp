"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, Users, Send, Star, MapPin, Clock, CreditCard, Plus, Filter } from "lucide-react"
import Image from "next/image"
import { redirect } from 'next/navigation';

const mockLoans = [
  {
    id: 1,
    borrower: "Maria Santos",
    avatar: "/placeholder.svg?height=40&width=40",
    location: "Philippines → USA",
    amount: 2500,
    purpose: "Family medical emergency",
    creditScore: 785,
    interestRate: 8.5,
    term: "6 months",
    remittanceHistory: 24,
    totalRemittances: 45000,
    rating: 4.8,
  },
  {
    id: 2,
    borrower: "Ahmed Hassan",
    avatar: "/placeholder.svg?height=40&width=40",
    location: "Egypt → UAE",
    amount: 1800,
    purpose: "Business expansion",
    creditScore: 720,
    interestRate: 9.2,
    term: "12 months",
    remittanceHistory: 18,
    totalRemittances: 32000,
    rating: 4.6,
  },
  {
    id: 3,
    borrower: "Rosa Martinez",
    avatar: "/placeholder.svg?height=40&width=40",
    location: "Mexico → USA",
    amount: 3200,
    purpose: "Home renovation",
    creditScore: 650,
    interestRate: 11.8,
    term: "9 months",
    remittanceHistory: 12,
    totalRemittances: 28000,
    rating: 4.3,
  },
]

const mockRemittances = [
  { id: 1, recipient: "Maria Santos", amount: 500, date: "2024-01-15", status: "Completed" },
  { id: 2, recipient: "Juan Rodriguez", amount: 750, date: "2024-01-10", status: "Completed" },
  { id: 3, recipient: "Ana Garcia", amount: 300, date: "2024-01-05", status: "Pending" },
]

function getCreditScoreColor(score: number) {
  if (score >= 750) return "text-green-600"
  if (score >= 650) return "text-yellow-600"
  return "text-red-600"
}

function getCreditScoreLabel(score: number) {
  if (score >= 750) return "Excellent"
  if (score >= 650) return "Good"
  return "Fair"
}

export default function MicroloanApp() {
  const [activeTab, setActiveTab] = useState("marketplace")
  const [loanAmount, setLoanAmount] = useState("")
  const [loanPurpose, setLoanPurpose] = useState("")
  const [loanTerm, setLoanTerm] = useState("")
  const [remittanceAmount, setRemittanceAmount] = useState("")
  const [remittanceRecipient, setRemittanceRecipient] = useState("")

  const handleLoanApplication = () => {
    // Handle loan application logic
    console.log("Loan application submitted:", { loanAmount, loanPurpose, loanTerm })
  }

  const handleRemittance = () => {
    // Handle remittance logic
    console.log("Remittance sent:", { remittanceAmount, remittanceRecipient })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Image src="/mygrant.png" alt="Microloan App Logo" height={140} width={140} />
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm">
              <CreditCard className="h-4 w-4 mr-2" />
              Wallet: $1,250
            </Button>
            <Avatar>
              <AvatarImage src="/placeholder.svg?height=32&width=32" />
              <AvatarFallback>JD</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Loans</p>
                  <p className="text-2xl font-bold">$12,450</p>
                </div>
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Loans</p>
                  <p className="text-2xl font-bold">3</p>
                </div>
                <Users className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Credit Score</p>
                  <p className="text-2xl font-bold text-green-600">785</p>
                </div>
                <Star className="h-8 w-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Remittances</p>
                  <p className="text-2xl font-bold">$45,200</p>
                </div>
                <Send className="h-8 w-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="marketplace">Marketplace</TabsTrigger>
            <TabsTrigger value="borrow">Borrow</TabsTrigger>
            <TabsTrigger value="lend">Lend</TabsTrigger>
            <TabsTrigger value="remittances">Remittances</TabsTrigger>
          </TabsList>

          {/* Marketplace Tab */}
          <TabsContent value="marketplace" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Loan Marketplace</h2>
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
            </div>

            <div className="grid gap-6">
              {mockLoans.map((loan) => (
                <Card key={loan.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4">
                        <Avatar className="h-12 w-12">
                          <AvatarImage src={loan.avatar || "/placeholder.svg"} />
                          <AvatarFallback>
                            {loan.borrower
                              .split(" ")
                              .map((n) => n[0])
                              .join("")}
                          </AvatarFallback>
                        </Avatar>
                        <div className="space-y-2">
                          <div>
                            <h3 className="font-semibold text-lg">{loan.borrower}</h3>
                            <div className="flex items-center text-sm text-gray-600">
                              <MapPin className="h-4 w-4 mr-1" />
                              {loan.location}
                            </div>
                          </div>
                          <p className="text-gray-700">{loan.purpose}</p>
                          <div className="flex items-center space-x-4 text-sm">
                            <div className="flex items-center">
                              <Star className="h-4 w-4 text-yellow-500 mr-1" />
                              {loan.rating}
                            </div>
                            <div className="flex items-center">
                              <Clock className="h-4 w-4 text-gray-500 mr-1" />
                              {loan.remittanceHistory} months history
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="text-right space-y-2">
                        <div className="text-2xl font-bold">${loan.amount.toLocaleString()}</div>
                        <div className="space-y-1">
                          <div className="flex items-center justify-end space-x-2">
                            <span className="text-sm text-gray-600">Credit Score:</span>
                            <Badge variant="outline" className={getCreditScoreColor(loan.creditScore)}>
                              {loan.creditScore} - {getCreditScoreLabel(loan.creditScore)}
                            </Badge>
                          </div>
                          <div className="text-sm text-gray-600">
                            Interest: <span className="font-semibold">{loan.interestRate}%</span>
                          </div>
                          <div className="text-sm text-gray-600">Term: {loan.term}</div>
                        </div>
                        <Button className="w-full">Lend Money</Button>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t">
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Total Remittances:</span>
                          <span className="ml-2 font-semibold">${loan.totalRemittances.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Remittance History:</span>
                          <span className="ml-2 font-semibold">{loan.remittanceHistory} months</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Borrow Tab */}
          <TabsContent value="borrow" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Apply for a Loan</CardTitle>
                <CardDescription>
                  Get quick access to funds based on your remittance history and credit score.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="amount">Loan Amount</Label>
                    <Input
                      id="amount"
                      placeholder="Enter amount"
                      value={loanAmount}
                      onChange={(e) => setLoanAmount(e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="term">Loan Term</Label>
                    <Select value={loanTerm} onValueChange={setLoanTerm}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select term" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="3">3 months</SelectItem>
                        <SelectItem value="6">6 months</SelectItem>
                        <SelectItem value="9">9 months</SelectItem>
                        <SelectItem value="12">12 months</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="purpose">Purpose of Loan</Label>
                  <Textarea
                    id="purpose"
                    placeholder="Describe why you need this loan"
                    value={loanPurpose}
                    onChange={(e) => setLoanPurpose(e.target.value)}
                  />
                </div>

                {/* Credit Score Display */}
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">Your Credit Profile</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Credit Score</p>
                      <p className="text-lg font-bold text-green-600">785 - Excellent</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Estimated Interest Rate</p>
                      <p className="text-lg font-bold">8.5%</p>
                    </div>
                  </div>
                  <div className="mt-2">
                    <p className="text-sm text-gray-600">Based on 24 months of remittance history</p>
                    <Progress value={85} className="mt-1" />
                  </div>
                </div>

                <Button onClick={handleLoanApplication} className="w-full">
                  Submit Loan Application
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Lend Tab */}
          <TabsContent value="lend" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Become a Lender</CardTitle>
                <CardDescription>
                  Help fellow migrant workers by providing loans and earn competitive returns.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Lending Benefits</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Earn 8-12% annual returns</li>
                    <li>• Support your community</li>
                    <li>• Diversify across multiple borrowers</li>
                    <li>• Transparent credit scoring system</li>
                  </ul>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-green-600">8.5%</div>
                      <div className="text-sm text-gray-600">Avg. Return</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-blue-600">95%</div>
                      <div className="text-sm text-gray-600">Repayment Rate</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-purple-600">$50</div>
                      <div className="text-sm text-gray-600">Min. Investment</div>
                    </CardContent>
                  </Card>
                </div>

                <Button className="w-full">
                  <Plus className="h-4 w-4 mr-2" />
                  Start Lending
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Remittances Tab */}
          <TabsContent value="remittances" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Send Remittance */}
              <Card>
                <CardHeader>
                  <CardTitle>Send Money</CardTitle>
                  <CardDescription>
                    Send money to family and friends. Your remittance history helps build your credit score.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="recipient">Recipient</Label>
                    <Input
                      id="recipient"
                      placeholder="Enter recipient name"
                      value={remittanceRecipient}
                      onChange={(e) => setRemittanceRecipient(e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="remittance-amount">Amount</Label>
                    <Input
                      id="remittance-amount"
                      placeholder="Enter amount"
                      value={remittanceAmount}
                      onChange={(e) => setRemittanceAmount(e.target.value)}
                    />
                  </div>
                  <div className="bg-green-50 p-3 rounded-lg">
                    <p className="text-sm text-green-800">
                      💡 Regular remittances improve your credit score and unlock better loan rates!
                    </p>
                  </div>
                  <Button onClick={handleRemittance} className="w-full">
                    <Send className="h-4 w-4 mr-2" />
                    Send Money
                  </Button>
                </CardContent>
              </Card>

              {/* Recent Remittances */}
              <Card>
                <CardHeader>
                  <CardTitle>Recent Remittances</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {mockRemittances.map((remittance) => (
                      <div key={remittance.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">{remittance.recipient}</p>
                          <p className="text-sm text-gray-600">{remittance.date}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">${remittance.amount}</p>
                          <Badge variant={remittance.status === "Completed" ? "default" : "secondary"}>
                            {remittance.status}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
