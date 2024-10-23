"use client";

import { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  PlusCircle,
  MinusCircle,
  ChevronLeft,
  ChevronRight,
  CircleCheckBig,
  CircleX,
} from "lucide-react";
import RuleTree from "./_components/rule-tree";
import {
  createRule,
  combineRules,
  evaluateRule,
  getCatalog,
  getAllRuleNames,
  getRule,
  deleteRule,
  modifyRule,
} from "./api/route";
import { toast, Toaster } from "sonner";

export default function RuleEngine() {
  const [ruleName, setRuleName] = useState("");
  const [ruleString, setRuleString] = useState("");
  const [activeRule, setActiveRule] = useState("");
  const [rules, setRules] = useState([]);
  const [combinedRules, setCombinedRules] = useState(["", ""]);
  const [isAndOperation, setIsAndOperation] = useState(true);
  const [evaluateRuleName, setEvaluateRuleName] = useState("");
  const [modifyRuleName, setModifyRuleName] = useState("");
  const [modifyRuleString, setModifyRuleString] = useState("");
  const [jsonData, setJsonData] = useState("");
  const [result, setResult] = useState(null);
  const [treeData, setTreeData] = useState(null);
  const [catalog, setCatalog] = useState({});
  const [isCatalogCollapsed, setIsCatalogCollapsed] = useState(false);

  const updateCatalog = useCallback(async () => {
    try {
      const response = await getCatalog();
      setCatalog(response);
    } catch (error) {
      console.error("Error getting catalog:", error);
      toast.error("Failed to update catalog");
    }
  }, []);

  const getRules = useCallback(async () => {
    try {
      const response = await getAllRuleNames();
      setRules(response);
    } catch (error) {
      console.error("Error getting rules:", error);
      toast.error("Failed to fetch rules");
    }
  }, []);

  const setTree = async (ruleName: string) => {
    try {
      const response = await getRule(ruleName);
      setTreeData(response);
      updateCatalog();
      toast.success(ruleName);
    } catch (error) {
      console.error("Error getting rule:", error);
      toast.error("Failed", { description: error as string });
    }
  };

  useEffect(() => {
    updateCatalog();
    getRules();
  }, [updateCatalog, getRules]);

  useEffect(() => {
    if (activeRule) {
      setTree(activeRule);
    }
  }, [activeRule]);

  useEffect(() => {
    setActiveRule(evaluateRuleName)
  }, [evaluateRuleName]);

    useEffect(() => {
    setActiveRule(modifyRuleName)
  }, [modifyRuleName]);

  const handleCreateRule = async () => {
    if (!ruleName.trim() || !ruleString.trim()) {
      toast.error("Rule name and string are required");
      return;
    }
    try {
      await createRule(ruleName, ruleString);
      setActiveRule(ruleName);
      await updateCatalog();
      await getRules();
      toast.success("Rule created successfully");
    } catch (error) {
      console.error("Error creating rule:", error);
      toast.error("Failed to create rule", { description: error as string });
    }
  };

  const handleEvaluateRule = async () => {
    if (!evaluateRuleName.trim() || !jsonData.trim()) {
      toast.error("Rule name and JSON data are required");
      return;
    }
    try {
      const data = JSON.parse(jsonData);
      if (data && typeof data !== "object") {
        throw new SyntaxError();
      }
      const response = await evaluateRule(evaluateRuleName, data);
      setResult(response.result);
      toast.success("Rule evaluated successfully");
    } catch (error) {
      console.error("Error evaluating rule:", error);
      if (error instanceof SyntaxError) {
        toast.error("Invalid JSON format. Please provide valid JSON.");
      } else {
        toast.error("Failed to evaluate rule", {
          description: error as string,
        });
      }
    }
  };

  const handleModifyRule = async () => {
    if (!modifyRuleName.trim() || !modifyRuleString.trim()) {
      toast.error("Rule name and string are required");
      return;
    }
    try {
      const response = await modifyRule(modifyRuleName, modifyRuleString);
      await updateCatalog();
      await getRules();
      setTreeData(response);
      toast.success("Rule modified successfully");
    } catch (error) {
      console.error("Error modifying rule:", error);
      toast.error("Failed to modify rule", { description: error as string });
    }
  };

  const handleDeleteRule = async () => {
    if (!activeRule.trim()) {
      toast.error("Rule name is required");
      return;
    }
    try {
      await deleteRule(activeRule);
      await getRules();
      toast.success("Rule deleted successfully");
    } catch (error) {
      console.error("Error deleting rule:", error);
      toast.error("Failed to delete rule", { description: error as string });
    }
  }
  // Combine rules helper functions
  const handleCombineRules = async () => {
    if (combinedRules.some((rule) => !rule.trim())) {
      toast.error("All rule fields must be filled");
      return;
    }
    try {
      const response = await combineRules(
        combinedRules,
        isAndOperation ? "AND" : "OR"
      );
      setTreeData(response);
      await updateCatalog();
      await getRules();
      toast.success("Rules combined successfully");
    } catch (error) {
      console.error("Error combining rules:", error);
      toast.error("Failed to combine rules", { description: error as string });
    }
  };

  const handleAddRule = () => {
    setCombinedRules([...combinedRules, ""]);
  };

  const handleRemoveRule = (index: number) => {
    if (combinedRules.length > 2) {
      const newRules = combinedRules.filter((_, i) => i !== index);
      setCombinedRules(newRules);
    }
  };

  const handleRuleChange = (index: number, value: string) => {
    const newRules = [...combinedRules];
    newRules[index] = value;
    setCombinedRules(newRules);
  };

  return (
    <div className="flex h-screen">
      <Toaster position="top-right" />
      {/* catalog section */}
      <aside
        className={`bg-gray-100 p-4 transition-all duration-300 ease-in-out ${
          isCatalogCollapsed ? "w-12" : "w-64"
        }`}
      >
        <div className="flex justify-between items-center mb-4">
          <h2
            className={`font-bold ${isCatalogCollapsed ? "sr-only" : "block"}`}
          >
            Catalog
          </h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCatalogCollapsed(!isCatalogCollapsed)}
            aria-label={
              isCatalogCollapsed ? "Expand catalog" : "Collapse catalog"
            }
          >
            {isCatalogCollapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </Button>
        </div>
        {!isCatalogCollapsed && catalog && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Property</TableHead>
                <TableHead>Type</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(catalog).map(([property, type]) => (
                <TableRow key={property}>
                  <TableCell>{property}</TableCell>
                  <TableCell>{type as string}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </aside>

      {/* rule engine section */}
      <main className="flex-1 p-4 overflow-auto">
        <h1 className="text-2xl font-bold mb-4">Rule Engine</h1>
        <Tabs defaultValue="create">
          <TabsList>
            <TabsTrigger value="create">Create Rule</TabsTrigger>
            <TabsTrigger value="combine">Combine Rules</TabsTrigger>
            <TabsTrigger value="evaluate">Evaluate Rule</TabsTrigger>
            <TabsTrigger value="modify">Modify Rule</TabsTrigger>
          </TabsList>
          <TabsContent value="create">
            <Card>
              <CardHeader>
                <CardTitle>Create Rule</CardTitle>
              </CardHeader>
              <CardContent>
                <Input
                  placeholder="Enter rule name..."
                  value={ruleName}
                  onChange={(e) => setRuleName(e.target.value)}
                  className="mb-4"
                />
                <Textarea
                  placeholder="Enter rule string..."
                  value={ruleString}
                  onChange={(e) => setRuleString(e.target.value)}
                  className="mt-4"
                />
                <Button onClick={handleCreateRule} className="mt-4">Create Rule</Button>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="combine">
            <Card>
              <CardHeader>
                <CardTitle>Combine Rules</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-2 mb-4">
                  <Switch
                    id="operation-mode"
                    checked={isAndOperation}
                    onCheckedChange={setIsAndOperation}
                  />
                  <Label htmlFor="operation-mode">
                    {isAndOperation ? "AND" : "OR"} Operation
                  </Label>
                </div>
                {combinedRules.map((rule, index) => (
                  <div key={index} className="flex items-center mb-4">
                    <Input
                      placeholder={`Enter rule ${index + 1}...`}
                      value={rule}
                      onChange={(e) => handleRuleChange(index, e.target.value)}
                      className="flex-grow"
                    />
                    {combinedRules.length > 2 && (
                      <Button
                        onClick={() => handleRemoveRule(index)}
                        variant="outline"
                        size="icon"
                        className="ml-2"
                      >
                        <MinusCircle className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
                <div className="flex space-x-2 mb-4">
                  <Button onClick={handleAddRule} variant="outline">
                    <PlusCircle className="mr-2 h-4 w-4" /> Add Rule
                  </Button>
                  <Button onClick={handleCombineRules}>Combine Rules</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="evaluate">
            <Card>
              <CardHeader>
                <CardTitle>Evaluate Rule</CardTitle>
              </CardHeader>
              <CardContent>
                <Select onValueChange={setEvaluateRuleName}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select rule to evaluate" />
                  </SelectTrigger>
                  <SelectContent>
                    {rules.map((rule) => (
                      <SelectItem key={rule} value={rule}>
                        {rule}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Textarea
                  placeholder="Enter JSON data..."
                  value={jsonData}
                  onChange={(e) => setJsonData(e.target.value)}
                  className="mt-4"
                />
                <Button onClick={handleEvaluateRule} className="mt-4">
                  Evaluate Rule
                </Button>
                {result !== null && (
                  <div className="mt-4">
                    <Button variant="ghost">Result: </Button>
                    {result ? (
                      <Button variant="outline">
                        <CircleCheckBig /> True
                      </Button>
                    ) : (
                      <Button variant="destructive">
                        <CircleX /> False
                      </Button>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="modify">
            <Card>
              <CardHeader>
                <CardTitle>Modify Rule</CardTitle>
              </CardHeader>
              <CardContent>
                <Select onValueChange={setModifyRuleName}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select rule to modify" />
                  </SelectTrigger>
                  <SelectContent>
                    {rules.map((rule) => (
                      <SelectItem key={rule} value={rule}>
                        {rule}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Textarea
                  placeholder="Enter new rule string..."
                  value={modifyRuleString}
                  onChange={(e) => setModifyRuleString(e.target.value)}
                  className="mt-4"
                />
                <Button onClick={handleModifyRule} className="mt-4">
                  Modify Rule
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
        <Card className="mt-4">
          <CardContent>
            <div style={{ width: "100%", height: "560px" }}>
              <div className="flex flex-row justify-between">
                <Button className="rounded-none">Rule Tree</Button>
                <div className="flex flex-row space-x-2">
                  <Select onValueChange={setActiveRule}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder={activeRule || "select rule"} />
                    </SelectTrigger>
                    <SelectContent>
                      {rules.map((rule) => (
                        <SelectItem key={rule} value={rule}>
                          {rule}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button
                    onClick={handleDeleteRule}
                    variant="destructive"
                    disabled={!activeRule}
                  >
                    Delete
                  </Button>
                </div>
              </div>
              {treeData && <RuleTree root={treeData} />}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
